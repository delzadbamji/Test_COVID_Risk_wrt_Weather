import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
# # "Afghanistan"
country = input("enter country")
# country="Ukraine"
file = 'dataset\\' + country + '.csv'

table = pd.read_csv(file,delimiter=',', usecols=['date','confirmed','deaths',
                                                    'recovered','humidity_mean','dew_mean','mean_ozone',
                                                    'mean_precip','mean_tMax','mean_tMin','mean_uv'])
y=input('add deaths,confirmed,recovered')
x= input('add weather data')
print(table)


import matplotlib.pyplot as plt
fig = plt.figure(1)	#identifies the figure
plt.title(country, fontsize='16')	#title
# plt.scatter(table["humidity_mean"], table["confirmed"])	#plot the points
plt.bar(table[x], table[y])
plt.hist2d(table[x], table[y])
plt.xlim([min(table[x]), max(table[x])])
plt.ylim([min(table[y]),max(table[y])+50])
plt.xlabel(x,fontsize='13')	#adds a label in the x axis

plt.ylabel(y,fontsize='13')	#adds a label in the y axis
plt.legend(x, loc='best')	#creates a legend to identify the plot

if not os.path.exists(country):
    os.mkdir(country)
plt.savefig(country+'\\'+country+'_'+x+'_'+y+'.png')	#saves the figure in the present directory
plt.grid()	#shows a grid under the plot
plt.show()




