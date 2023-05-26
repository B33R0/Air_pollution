import requests
import json
import datetime
import sqlite3
import time

conn = sqlite3.connect("air_pollution.sqlite")
curr = conn.cursor()
curr.execute(""" CREATE TABLE IF NOT EXISTS Air_pollution_tracker(
                    City TEXT,
                    Datetime DATETIME,
                    Quality TEXT,
                    Carbon_Monoxide REAL,
                    Nitrogen_Monoxide REAL,
                    Nitrogen_Dioxide REAL,
                    Ozone REAL,
                    Sulphur_dioxide REAL,
                    Fine_particles REAL,
                    Fine_particulate REAL,
                    Ammonia REAL

)
""")

key = 'e52eac6a4f1141f035f60281926c179c'
url_pol = "https://api.openweathermap.org/data/2.5/air_pollution"
url_geo = "https://api.openweathermap.org/geo/1.0/direct"
answer = int(input("if you want realtime info type 1 \nif you want specific time type 2: "))


def geocode(city):
    params = {"q": city, "limit": 5, "appid": key}
    response = requests.get(url_geo, params=params)
    data = response.text
    res_data = json.loads(data)
    return res_data[0]['lat'], res_data[0]['lon']


def unix_time(y, m, d, h, mins, s):
    epoch = int(datetime.datetime.strptime(datetime.datetime(y, m, d, h, mins, s).strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S").timestamp())
    return epoch


def unix_time_inverted(epoch):
    date = datetime.datetime.fromtimestamp(epoch).strftime('%d/%m/%Y %H:%M:%S')
    date_type = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M:%S')
    return date_type


def pollution_data(lat, lon, dt):
    if answer == 1:
        time.sleep(0.00001)
        params = {"lat": lat, "lon": lon, "appid": key}
        time.sleep(0.00001)
        response = requests.get(url_pol, params=params)
        time.sleep(0.00001)
        data = response.text
        res_data = json.loads(data)
        return res_data['list'][0]['components']
    else:
        time.sleep(0.00001)
        params = {"lat": lat, "lon": lon, "start": dt - 25, "end": dt, "appid": key}
        time.sleep(0.00001)
        response = requests.get(url_pol, params=params)
        time.sleep(0.00001)
        data = response.text
        res_data = json.loads(data)
        return res_data['list'][0]['components']


def quality(co):
    if 0 <= co <= 20:
        return "Good"
    elif 20 < co <= 80:
        return "Fair"
    elif 80 < co <= 250:
        return "Moderate"
    elif 250 < co <= 350:
        return "Poor"
    else:
        return "Very Poor"


city_name = str(input("input city: "))
lat1 = geocode(city_name)[0]
lon1 = geocode(city_name)[1]

if answer == 2:
    year = int(input("Input year(1970-today): "))
    month = int(input("Input month(1-12): "))
    day = int(input("Input day1-31: "))
    hour = int(input("Input hour(24hr format): "))
    minutes = int(input("Input minutes: "))
    seconds = int(input("Input seconds: "))
    date = unix_time(year, month, day, hour, minutes, seconds)
    db_date = unix_time_inverted(unix_time(year, month, day, hour, minutes, seconds))
    print(
        f'    On this date- {unix_time_inverted(date)} in {city_name} air quality was {quality(pollution_data(lat1, lon1, date)["co"])}.'
        f'\nThe air consisted of:'
        f'\nCarbon monoxide: {pollution_data(lat1, lon1, date)["co"]}μg/m3'
        f'\nNitrogen monoxide: {pollution_data(lat1, lon1, date)["no"]}μg/m3'
        f'\nNitrogen dioxide: {pollution_data(lat1, lon1, date)["no2"]}μg/m3'
        f'\nOzone: {pollution_data(lat1, lon1, date)["o3"]}μg/m3'
        f'\nSulphur dioxide: {pollution_data(lat1, lon1, date)["so2"]}μg/m3'
        f'\nFine particles matter: {pollution_data(lat1, lon1, date)["pm2_5"]}μg/m3'
        f'\nCoarse particulate matter: {pollution_data(lat1, lon1, date)["pm10"]}μg/m3'
        f'\nAmmonia: {pollution_data(lat1, lon1, date)["nh3"]}μg/m3')


else:
    date = None
    db_date = datetime.date.today()
    print(f'    Today in {city_name} air quality is {quality(pollution_data(lat1, lon1, date)["co"])}.'
          f'\nThe air consisted of:'
          f'\nCarbon monoxide: {pollution_data(lat1, lon1, date)["co"]}μg/m3'
          f'\nNitrogen monoxide: {pollution_data(lat1, lon1, date)["no"]}μg/m3'
          f'\nNitrogen dioxide: {pollution_data(lat1, lon1, date)["no2"]}μg/m3'
          f'\nOzone: {pollution_data(lat1, lon1, date)["o3"]}μg/m3'
          f'\nSulphur dioxide: {pollution_data(lat1, lon1, date)["so2"]}μg/m3'
          f'\nFine particles matter: {pollution_data(lat1, lon1, date)["pm2_5"]}μg/m3'
          f'\nCoarse particulate matter: {pollution_data(lat1, lon1, date)["pm10"]}μg/m3'
          f'\nAmmonia: {pollution_data(lat1, lon1, date)["nh3"]}μg/m3')

"""
This will store air pollution data with city and date and it
can be accessible in the database.
"""
curr.execute(
    "INSERT INTO Air_pollution_tracker (City, Datetime, Quality, Carbon_Monoxide, Nitrogen_Monoxide, Nitrogen_Dioxide, Ozone, "
    "Sulphur_dioxide, Fine_particles, Fine_particulate, Ammonia) "
    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (city_name, db_date, quality(pollution_data(lat1, lon1, date)["co"]),
                                                 pollution_data(lat1, lon1, date)["co"],
                                                 pollution_data(lat1, lon1, date)["no"],
                                                 pollution_data(lat1, lon1, date)["no2"],
                                                 pollution_data(lat1, lon1, date)["o3"],
                                                 pollution_data(lat1, lon1, date)["so2"],
                                                 pollution_data(lat1, lon1, date)["pm2_5"],
                                                 pollution_data(lat1, lon1, date)["pm10"],
                                                 pollution_data(lat1, lon1, date)["nh3"]))
conn.commit()
conn.close()