import os
import sqlite3

import pandas as pd
from tqdm import tqdm

conn = None
try:
    conn = sqlite3.connect("coviddb.db")

except Exception as e:
    raise Exception('errors in the db creation')

tablestr = '''CREATE TABLE IF NOT EXISTS country_data (id integer PRIMARY KEY,
                country text,date date NOT NULL,
           confirmed integer, risk integer, recovered integer,humidity_mean real,humidity_std real,dew_mean real,
          dew_std real, mean_ozone real,std_ozone real, mean_precip real, std_precip real,mean_tMax real,std_tMax real,
          mean_tMin real,std_tMin real,mean_uv real,std_uv real);
           '''
# country	date	confirmed	deaths	recovered	humidity_mean	humidity_std	dew_mean	dew_std	mean_ozone
# std_ozone	mean_precip	std_precip	mean_tMax	std_tMax	mean_tMin	std_tMin	mean_uv	std_uv

if conn is not None:
    try:
        c = conn.cursor()
        c.execute(tablestr)
    except Exception as e:
        raise Exception('errors in the table creation')


sql = '''INSERT INTO country_data(id,country,date, confirmed, risk, recovered,humidity_mean,humidity_std,dew_mean,
    dew_std, mean_ozone,std_ozone , mean_precip , std_precip ,mean_tMax ,std_tMax ,mean_tMin ,std_tMin ,mean_uv ,std_uv) 
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

ids = 0  # primary key

print("COVID-19 data for Countries shall begin loading shortly.....")
for file in tqdm(os.listdir("Country_dataset")):


    df = pd.read_csv("Country_dataset/" + file)

    # print(df)
    '''mean death count to replace death column as risk'''
    death_count = df.describe()['deaths']['mean']
    # print("dead mean: ",death_count)
    '''for each row in df'''
    for index, row in df.iterrows():
        # print(row)
        risk = 0 if row['deaths'] < death_count else 1
        # print(row['deaths'])
        # print(risk)
        ''' create a list to add to the db'''
        setbuilder = [ids, row['# country'], row['date'], row['confirmed'],risk, row['recovered'], row['humidity_mean'],
                      row['humidity_std'],	row['dew_mean'], row['dew_std'],	row['mean_ozone'], row['std_ozone'],
                      row['mean_precip'],	row['std_precip'],	row['mean_tMax'],	row['std_tMax'], row['mean_tMin'],
                      row['std_tMin'],	row['mean_uv'],	row['std_uv']]

        # country	date	confirmed	deaths	recovered	humidity_mean	humidity_std	dew_mean	dew_std	mean_ozone
        # std_ozone	mean_precip	std_precip	mean_tMax	std_tMax	mean_tMin	std_tMin	mean_uv	std_uv

        # print(setbuilder)

        ids += 1  # increment the id for uniqueness in the primary key



        try:
            cur = conn.cursor()
            cur.execute(sql, setbuilder)
            conn.commit()
        except Exception as e:
            raise Exception('errors in the table') from e
#
# conn.close()