from tqdm import tqdm
import psycopg2
import pandas as pd
import subprocess
import ast

DB_HOST = 'localhost'
DB_NAME = 'us'
DB_USER = 'postgres'
DB_PASS = 'buddyrich134'
conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
cursor = conn.cursor()
cursor.execute("SELECT distinct code from public.maincode;")
conn.commit()
codelist = [i[0] for i in cursor.fetchall()]
list_ = []
for code in tqdm(codelist):
    try:
        command = "zacks-api " + code
        result = subprocess.check_output(command, shell=True)
        res = ast.literal_eval(result.decode("utf-8"))
# Parse the result as JSON
        da = res["updatedAt"]
        rank = res['zacksRank']
        list_.append([da, code, rank])
    except Exception as e:
        print(f"{code} passed {e}")
        pass
cursor.executemany("INSERT INTO public.zacksRank (da, code, rank) VALUES (%s, %s, %s)", list_)
conn.commit()