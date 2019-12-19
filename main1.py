import requests as http
from pprint import pprint as pp
import json

#adding some text
# connection = pymysql.connect(
#     host='localhost',
#     user='user',
#     password='passwd',
#     db='db',
#     charset='utf8mb4',
#     cursorclass=pymysql.cursors.DictCursor
# )
# cursor = connection.cursor()
stations_response = http.get('http://api.gios.gov.pl/pjp-api/rest/station/findAll')
if stations_response.status_code != 200:
        raise SystemExit('Błąd połączenia')
stations_data = stations_response.json()


full_measures_data = []


for station in stations_data:

    if not station['city']:
        continue

    station_sensors_response = http.get(
        f'http://api.gios.gov.pl/pjp-api/rest/station/sensors/{station["id"]}'
    )
    station_sensors_data = station_sensors_response.json()

    for sensor in station_sensors_data:

        sensor_measures_response = http.get(
            f'http://api.gios.gov.pl/pjp-api/rest/data/getData/{sensor["id"]}'
        )
        sensor_measures_data = sensor_measures_response.json()

        for single_measure in sensor_measures_data['values']:
            measure_data = {
                'measure_date': single_measure['date'],
                'measure_value': single_measure['value'],
                'measure_sensor_id': sensor['id'],
                'measure_sensor_param_id': sensor['param']['idParam'],
                'measure_sensor_param_code': sensor['param']['paramCode'],
                'measure_sensor_param_name': sensor['param']['paramName'],
                'measure_station_id': station['id'],
                'measure_station_name': station['stationName'],
                'measure_station_city': station['city']['commune']['communeName'],
                'measure_station_province': station['city']['commune']['provinceName'],
                'measure_station_lon': station['gegrLon'],
                'measure_station_lat': station['gegrLat']
            }
            full_measures_data.append(measure_data)
            break


pp(full_measures_data).head()

f = open('data.json', 'w', encoding='utf-8')
f.write(json.dumps(full_measures_data))
f.close()




