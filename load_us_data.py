import os
import sqlite3

import pandas as pd
from tqdm import tqdm

conn = None
try:
    conn = sqlite3.connect("coviddb.db")

except Exception as e:
    raise Exception('errors in the db creation')

tablestr = "CREATE TABLE IF NOT EXISTS us_data (id integer PRIMARY KEY, " \
           "date date NOT NULL, Province text not null, lat real, longi real, " \
           "confirmed integer, risk integer, recovered integer, active integer," \
           " incident_rate real, total_test integer,fatality_ratio real);"

if conn is not None:
    try:
        c = conn.cursor()
        c.execute(tablestr)
    except Exception as e:
        raise Exception('errors in the table creation')

sql = '''INSERT INTO us_data(id,date,Province,lat,longi,confirmed,risk, recovered, active,incident_rate,
total_test,fatality_ratio) VALUES(?,?,?,?,?,?,?,?,?,?,?,?) '''

ids = 0  # primary key

print("COVID-19 data for US states shall begin loading shortly.....")
for file in tqdm(os.listdir("daily_data_us")):

    # extract date from filename
    date = file.split(".")[0]

    # print(date)
    df = pd.read_csv("daily_data_us/" + file)

    '''mean death count to replace death column as risk'''
    death_count = df.describe()['Deaths']['mean']

    '''for each row in df'''
    for index, row in df.iterrows():
        # print(row)
        risk = 0 if row['Deaths'] < death_count else 1
        try:
            people_tested = row['People_Tested']
        except:
            people_tested = row['Total_Test_Results']
        try:
            mortality = row['Case_Fatality_Ratio']
        except:
            mortality = row['Mortality_Rate']

        # print(row['Deaths'])
        # print(risk)
        ''' create a list to add to the db'''
        setbuilder = [ids, date, row['Province_State'], row['Lat'], row['Long_'], row['Confirmed'],
                      risk, row['Recovered'], row['Active'], row['Incident_Rate'], people_tested, mortality]

        # print(setbuilder)

        ids += 1  # increment the id for uniqueness in the primary key

        try:
            cur = conn.cursor()
            cur.execute(sql, setbuilder)
            conn.commit()
        except Exception as e:
            raise Exception('errors in the table') from e

conn.close()
