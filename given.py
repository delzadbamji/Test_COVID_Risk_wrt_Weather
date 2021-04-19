import pandas as pd
import math
import statsmodels.api as sm
from scipy.stats import pearsonr
import numpy as np
import os

# import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams

def get_corr(df2):
    # print(df2.info())
    c = df2.corr()
    c[:] = np.where(c.eq('NaN'), 0, c)
    # c = c.replace('NaN', 0)
    # print(c)
    return c


def get_data(country):
    url = 'dataset/' + country + '.csv'
    dateparse = lambda dates: [pd.datetime.strptime(d, '%d-%m-%Y') for d in dates]
    df = pd.read_csv(url, parse_dates=True, date_parser=dateparse, index_col=1)
    # df['date'] = pd.to_datetime(df.date, format='%d/%m/%Y')
    master_col = 'active_case'
    active_case = df['confirmed'] - df['deaths'] - df['recovered']  # caluculate active case
    df2 = df[['humidity_mean', 'humidity_std', 'dew_mean', 'dew_std', 'mean_ozone', 'std_ozone',
              'mean_precip', 'std_precip', 'mean_tMax', 'std_tMax', 'mean_tMin', 'std_tMin', 'mean_uv',
              'std_uv']].copy()
    df2['active_case'] = active_case  # add active case
    c = get_corr(df2)

    return c


arr = os.listdir('dataset/')
# count_all = pd.read_csv('result.csv')
final_cor=np.zeros((15,15))
print(arr)
for c in(arr):

    country=c[:-4]
    print(c)
    if country not in ['Korea, South.csv']:
        c=get_data(country)
        npc=np.array(c)
        where_are_NaNs = np.isnan(npc)
        npc[where_are_NaNs] = 0
        print(npc)
        final_cor=final_cor+npc



        corr = final_cor
        corr=corr/169
        fig= plt.figure(figsize=(10,7))
        l=['Humidity (mean)', 'Humidity (std)', 'Dew (mean)', 'Dew (std)', 'Ozone (mean)',
               'Ozone (std)', 'Perception (mean)', 'Perception (std)', 'Max temp (mean)', 'Max temp (std)',
               'Min temp (mean)', 'Min temp (std)', 'UV (mean)', 'UV (std)', 'Active Case']
        sns.heatmap(corr,xticklabels=l, yticklabels=l,cmap="coolwarm")
        rcParams.update({'figure.autolayout': True})
        plt.savefig('cor.png',dpi=200)
