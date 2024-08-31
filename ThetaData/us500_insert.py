import requests
import threading
import time
from datetime import datetime, timedelta
import psycopg2
from IPython.display import display, clear_output
import warnings
warnings.filterwarnings('ignore')
class ContinuousProcessor:
    def __init__(self):
        self.url = 'http://127.0.0.1:25510/v2/snapshot/stock/trade?root='
        self.conn = self.get_db_connection()
        self.cursor = self.conn.cursor()
        self.load_stock_lists()
        self.market_open = False
    def get_db_connection(self):
        DB_HOST = 'localhost'
        DB_NAME = 'us'
        DB_USER = 'postgres'
        DB_PASS = 'buddyrich134'
        try:
            conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
            return conn
        except Exception as e:
            print(f"Database connection error: {e}")
            raise

    def load_stock_lists(self):
        try:
            # Load US500 stock codes
            self.cursor.execute("SELECT * FROM maincode WHERE listed = 'us500';")
            self.conn.commit()
            self.list_us500 = [i[0] for i in self.cursor.fetchall()]

            # Load US100 stock codes
            self.cursor.execute("SELECT * FROM maincode WHERE listed = 'us100';")
            self.conn.commit()
            self.list_us100 = [i[0] for i in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error loading stock lists: {e}")
            raise

    def fetch_stock_price(self, code):
        try:
            url = self.url + code
            res = requests.get(url).json()['response'][0]
            ms = res[0]
            price = res[-2]
            date_str = str(res[-1])
            
            milliseconds_of_day = ms
            seconds_of_day = milliseconds_of_day / 1000
            hours, remainder = divmod(seconds_of_day, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            date = datetime.strptime(date_str, '%Y%m%d')
            result_datetime = date + timedelta(hours=hours, minutes=minutes, seconds=seconds)
            formatted_datetime = result_datetime.strftime('%Y-%m-%d %H:%M:00')
            return [formatted_datetime, code, price]
        except Exception as e:
            print(f"An error occurred while fetching stock price for {code}: {e}")
            return None

    def continuous_loop(self):
        while True:
            try:
                clear_output(wait=True)
                now = datetime.now()
                if now.hour == 21 and now.minute == 30:
                    self.market_open = True
                else:
                    print(f"market not opened for {now}")
                    time.sleep(1)
                if self.market_open:
                    print(now)
                    list_stockprice = []
                    if now.minute % 5 == 0 and now.second <= 2:
                        for code in self.list_us500[:]:
                            data = self.fetch_stock_price(code)
                            if data:
                                list_stockprice.append(data)
                        self.cursor.executemany(
                            "INSERT INTO public.stock_price_5m (da, code, cl) VALUES (%s, %s, %s);",
                            list_stockprice
                        )
                        self.conn.commit()
                        print("Insert success")
                        list_stockprice = []
                        time.sleep(60 - now.second) 
                else:
                    time.sleep(5)
            except Exception as e:
                print(f"An error occurred in the continuous loop: {e}")
def main():
    processor = ContinuousProcessor()
    loop_thread = threading.Thread(target=processor.continuous_loop, daemon=True)
    loop_thread.start()

if __name__ == "__main__":
    main()
