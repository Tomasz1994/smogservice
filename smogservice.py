#najmlodsze daty
#utworzyc ramki dla wszystkich unikalnych nazw odczynnikow
#pogrupowanie po wojewodztwach i miastach
#dane dla odczytow min, max, avg
#do ramki finalnej dane geolokalizacyjne stacji (osi na wykresie wg geolokalizacji Polski)

import json
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
from dateutil.relativedelta import relativedelta

pd.set_option('display.max_columns', 100)
measure_per_code={}
param_code_mean ={}


with open('data2.json',encoding='utf-8') as f:
    measures_list = json.loads(f.read())
    measures_list_df = pd.DataFrame(measures_list)

measures_list_df['measure_date'] = pd.to_datetime(measures_list_df.measure_date)
#print('unique dates: ',measures_list_df['measure_date'].unique())
print(measures_list_df['measure_station_id'].count())


today = datetime.datetime.today()
border_date = today - relativedelta(days=7)
print('border_date: ',border_date)

measures_list_df = measures_list_df.loc[measures_list_df['measure_date'] > border_date]
#measures_list_df['new_lat']=measures_list_df['measure_station_lat'].astype(int)
measures_list_df['new_lat']=measures_list_df['measure_station_lat'].astype(str).astype(float)
measures_list_df['new_lon']=measures_list_df['measure_station_lon'].astype(str).astype(float)
print('typy pol  ', measures_list_df.dtypes)

print('lista kolumn: ',list(measures_list_df.columns))
#print(measures_list_df.head(5))

param_codes = measures_list_df['measure_sensor_param_code'].unique()
print('kody pomiarow: ', param_codes)

for param_code in param_codes:

    measure_per_code[param_code]=measures_list_df.loc[measures_list_df['measure_sensor_param_code'] == param_code]
    print('lista pol z nowym polem measure_per_code ', list(measure_per_code[param_code].keys()))
    #print(measure_per_code[param_code].head())

    if param_code not in param_code_mean:
        param_code_mean[param_code]=measure_per_code[param_code].loc[:,'measure_value'].mean()
        #print('w koncu srednia',measure_per_code[param_code].loc[:,'measure_value'].mean())

    measure_per_city = measure_per_code[param_code][['measure_station_city','measure_value','new_lon','new_lat']].groupby('measure_station_city').mean()

    print('lista pol  ',list(measure_per_city.keys()))
    print('typy pol  ', measure_per_city.dtypes)
    #print(measure_per_city.head())
    #print('type(measure_per_city)  ', type(measure_per_city))

    cathegories=measure_per_city['measure_value']
    #print('type(cathegories)  ', type(cathegories))
    cat=pd.cut(cathegories,np.r_[0,10,20,30,40])

    plt.scatter(measure_per_city['new_lon'],measure_per_city['new_lat'],color='red')

    #uwaga tu polozenie tekstu nalezy kazdorazowo dopasowac
    plt.text(20,50,'Jakis sobie text',fontsize=12)

    str = (param_code,' mean= ',param_code_mean[param_code])
    plt.title(str)
    plt.xlabel('gps longtitude')
    plt.ylabel('gps latitude')
    plt.show()
