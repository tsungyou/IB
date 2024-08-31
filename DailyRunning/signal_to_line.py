import pandas as pd
import psycopg2
from datetime import datetime
from config import *
import requests
import warnings
import time
import numpy as np
warnings.filterwarnings("ignore")

class SignalGenerator():
    def __init__(self):
        self.list_ = None
        self.init_minute = None
        self.iterator = 0
        self.rolling = 5
        self.benchmark = 2
        self.benchmark_index = "QQQ"
        self.conn = self.get_db_connection()
        self.cursor = self.conn.cursor()
        self.get_code_list(index='us100')
    def get_db_connection(self):
        conn = psycopg2.connect(host=DB_HOST, dbname='us', user=DB_USER, password=DB_PASS)
        return conn
    
    def get_code_list(self, index='us100'):
        self.cursor.execute(f"SELECT distinct code from public.maincode where listed = '{index}';")
        self.conn.commit()
        self.list_ = [i[0] for i in self.cursor.fetchall()]
        return None
    
    def lineNotify(self, code, direction, stdsize123, da):
        headers = {
            'Authorization': 'Bearer ' + LINE_TOKEN
        }
        data = {
            'message':f'''
            ========今天 {self.iterator} 個訊號 ==========
            code: {code}\n 
            direction: {direction}(1 for long, -1 for short)\n 
            current time:{datetime.now()}\n
            signal_time: {da} \n
            signal_value:{stdsize123} \n
            =============================================
            '''             
        }
        data = requests.post(LINE_URL, headers=headers, data=data)
        self.iterator += 1

    def backtest_strat1(self, code):
        '''
        abs(ret_diff - ret_mean)/ret_std
        '''
        self.cursor.execute(f"SELECT da, code, cl from public.stock_price where code in ('{code}', '{self.benchmark_index}') limit 20")
        self.conn.commit()
        df = pd.DataFrame(self.cursor.fetchall())
        df.columns = ['da','code', 'cl']
        pivoted = df.pivot(columns='code', values='cl', index='da')
        pivoted.ffill()
        ret = pivoted.pct_change()
        ret['ret_diff'] = ret[code] - ret[self.benchmark_index]
        ret['ret_diff_std'] = ret['ret_diff'].rolling(self.rolling).std() * 100
        ret['ret_diff_mean'] = ret['ret_diff'].rolling(self.rolling).mean() * 100
        ret['stdize_ret_diff'] = abs((ret['ret_diff'] - ret['ret_diff_mean'])/ret['ret_diff_std'])
        ret[code] = pivoted[code]
        ret[self.benchmark_index] = pivoted[self.benchmark_index]
        ret['da'] = pivoted.index
        last = ret.iloc[-1, :]
        if last['stdize_ret_diff'] >= self.benchmark:
            self.lineNotify(code, '1', np.round(last['stdize_ret_diff']), last['da'])
            return [last['da'], code]
    def backtest_strat2(self, code):
        try:
            self.cursor.execute(f"SELECT da, code, cl from public.stock_price where code in ('{code}', '{self.benchmark_index}') limit 20")
            self.conn.commit()
            df = pd.DataFrame(self.cursor.fetchall())
            df.columns = ['da','code', 'cl']
            pivoted = df.pivot(columns='code', values='cl', index='da')
            pivoted.ffill()
            ret = pivoted.pct_change()
            ret['stock_price'] = pivoted[code]
            ret['index_price'] = pivoted[self.benchmark_index]
            ret['ret_diff'] = ret[code] - ret[self.benchmark_index]
            # type 2
            ret['ret_diff_std'] = ret['ret_diff'].rolling(self.rolling).std()
            ret['ret_diff_mean'] = ret['ret_diff'].rolling(self.rolling).mean()
            ret['stdize_ret_diff'] = abs((ret['ret_diff'] - ret['ret_diff_mean'])*ret['ret_diff_std'])*10000

            # # check direction
            ret['lag10'] = ret['stock_price'].shift(5)
            ret['change_stock'] = (ret['stock_price'] - ret['lag10'])/ret['lag10']
            ret['direction'] = ret.apply(lambda x: -1 if x['stock_price'] - x['lag10'] > 0 else 1, axis=1)
            
            ret['change_twii'] = (ret['index_price'] - ret['lag10_twii'])/ret['lag10_twii']
            ret['filter_1'] = ret.apply(lambda x: 1 if abs(x['change_stock'] - x['change_twii']) < abs(x['change_stock']) else 0, axis=1)
            ret['filter_2'] = ret.apply(lambda x: 1 if abs(x['change_stock']) < abs(x['change_twii']) else 1, axis=1)
            last = ret.iloc[-1, :]
            da = last.index[-1]
            if last['stdize_ret_diff'] >= 2 and last['filter_1'] == 1 and last['filter_2'] == 1:
                self.lineNotify(code, last['direction'], last['stdize_ret_diff'], last['filter_1'])
        except Exception as e:
            print(e)
    def signal_generator(self):
        for code in self.list_:
            if code == self.benchmark_index: continue
            self.backtest_strat1(code)
        # for code in self.list_:
        #     if code == self.benchmark_index: continue
        #     self.backtest_strat2(code)
        
    def flow_controller(self):
        self.cursor.execute("SELECT da from public.stock_price order by da desc limit 1;")
        self.conn.commit()
        return self.cursor.fetchone()[0]
if __name__ == "__main__":
    sg = SignalGenerator()
    while True:
        da = sg.flow_controller()
        if sg.init_minute != da:
            sg.init_minute = da
            sg.signal_generator()
        else:
            time.sleep(60 - datetime.now().second + 3)