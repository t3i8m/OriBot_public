import requests
# from pprint import pprint
from datetime import datetime
from oribot_translator import translate_current_text
import pytz 
from timezonefinder import TimezoneFinder
# from tzwhere import tzwhere
# from zoneinfo import ZoneInfo




# API
open_meteo_api = "130173f2085b422b9bd132054232202"

weather_code_decode = {
    0:["Sunny", "☀️"],
    1:["Mainly clear", "🌤"],
    2:["Partly cloudy", "⛅"],
    3:["Overcast", "☁️"],
    45:["Fog", "🌫️"],
    48:["Fog", "🌫️"],
    51:["Light drizzle", "💧"],
    53:["Moderate drizzle", "💧💧"],
    55:["Dense drizzle", "💧💧💧"],
    56:["Light freezing drizzle", "❄️"],
    57:["Freezing drizzle", "🧊"],
    61:["Light rain", "🌦️"],
    63:["Moderate rain","🌨️"],
    65:["Heavy rain", "🌧️"],
    66:["Light freezing rain", "💧"],
    67:["Heavy freezing rain","🧊"],
    71:["Light snow", "🌨️"],
    73:["Moderate snow", "🌨️"],
    75:["Heavy snow", "🌨️"],
    77:["Snow grains", "🌨️"],
    80:["Light rain shower", "🌧️"],
    81:["Moderate rain shower", "🌨️"],
    82:["Heavy rain shower", "🌨️"],
    85:["Light snow showers", "🌨️"],
    86:["Heavy snow showers", "🌨️"],
    95:["Thunderstorm", "🌩️"],
    96:["Thunderstorm", "🌩️"],
    99:["Thunderstorm", "🌩️"]
}

weekdays = {1:"Monday",
            2:"Tuesday",
            3:"Wednesday",
            4:"Thursday",
            5:"Friday",
            6:"Saturday",
            7:"Sunday"}

def from_coordinates_to_location(long:int, lat:int)->(str):
    try:
        open_meteo_link = f"http://api.weatherapi.com/v1/forecast.json?key={open_meteo_api}&q={str(long)},{str(lat)}&days=7"
        response_open_meteo = requests.get(open_meteo_link, headers = {"User_Agent":"OriBot"}).json()
        # long_lat_dict = {
        # "City":response_open_meteo["location"],
        # "Long":response_open_meteo["location"]["lon"],
        # "Lat":response_open_meteo["location"]["lat"]
        # }
        # print(response_open_meteo)
        location = response_open_meteo["location"]["name"]+"/"+response_open_meteo["location"]["country"]
        return location
    except Exception as ex:
        print(ex)
        return False
    
def from_location_to_coordinates(location:str):
    try:
        print(location)
        open_meteo_link = f"http://api.weatherapi.com/v1/forecast.json?key={open_meteo_api}&q={str(location).lower()}&days=7"
        response_open_meteo = requests.get(open_meteo_link, headers = {"User_Agent":"OriBot"}).json()
        location_lat = response_open_meteo["location"]["lat"]
        location_long = response_open_meteo["location"]["lon"]
        location_full = response_open_meteo["location"]["name"]+"/"+response_open_meteo["location"]["country"]
        return [location_lat,location_long,location_full]
    except Exception as ex:
        print("from_location_to_coordinates()", ex)
        return False

    pass

def weather_main(user, period="7", method="basic")->(str):
    try:
        if method=="basic":
            url = f"https://api.open-meteo.com/v1/forecast?latitude={user.lat}&longitude={user.long}&hourly=temperature_2m,weathercode&daily=weathercode,temperature_2m_max,temperature_2m_min&timeformat=unixtime&timezone=auto&forecast_days={period}"
            location = user.location
            location_lat = user.lat
            location_long=user.long
        else:
            location = user["Location"]
            location_lat = user['Lat']
            location_long=user['Long']
            url = f"https://api.open-meteo.com/v1/forecast?latitude={user['Lat']}&longitude={user['Long']}&hourly=temperature_2m,weathercode&daily=weathercode,temperature_2m_max,temperature_2m_min&timeformat=unixtime&timezone=auto&forecast_days=2"

        response = requests.get(url, headers={"User-Agent":"OriBot"})
        weather = response.json()
        weather_container = {}

        for temp, time, code in zip(weather["hourly"]["temperature_2m"], weather["hourly"]["time"], weather["hourly"]["weathercode"]):
            # tz = tzwhere.tzwhere()
            # timezone_name = tz.tzNameAt(int(location_lat), int(location_long))
            # timezone = pytz.timezone(timezone_name)
            # datetime_object = datetime.fromtimestamp(time,timezone)
            # try:
            #     tf = TimezoneFinder()
            #     datetime_object = datetime.fromtimestamp(time,tz= pytz.timezone(tf.timezone_at(lat=location_lat, lng=location_long)))
            # except Exception as ex:
            datetime_object = datetime.fromtimestamp(time,pytz.timezone('Europe/London'))
            # if(datetime_object.date()>=datetime.now(pytz.timezone('Europe/London')).date()):
            if(datetime_object.date()>=datetime.now().date()):

                date_list = ["0"+str(n) if n<10 else n for n in [datetime_object.day, datetime_object.month]]
                current_date = str(date_list[0])+"."+str(date_list[1])+" ("+weekdays[datetime_object.isoweekday()]+")"
                if current_date not in weather_container.keys():
                    weather_container[current_date] = {"Forecast_for_day":{}}
                        
                if datetime_object.hour==0:
                    weather_container[current_date]["Forecast_for_day"]["00:00"] = [str(round(temp))+"°C", weather_code_decode[code][0]+" "+weather_code_decode[code][1]]
                elif datetime_object.hour==8:
                    weather_container[current_date]["Forecast_for_day"]["08:00"] = [str(round(temp))+"°C", weather_code_decode[code][0]+" "+weather_code_decode[code][1]]
                elif datetime_object.hour==12:
                    weather_container[current_date]["Forecast_for_day"]["12:00"] = [str(round(temp))+"°C", weather_code_decode[code][0]+" "+weather_code_decode[code][1]]
                elif datetime_object.hour==15:
                    weather_container[current_date]["Forecast_for_day"]["15:00"] = [str(round(temp))+"°C", weather_code_decode[code][0]+" "+weather_code_decode[code][1]]
                elif datetime_object.hour==18:
                    weather_container[current_date]["Forecast_for_day"]["18:00"] = [str(round(temp))+"°C", weather_code_decode[code][0]+" "+weather_code_decode[code][1]]
                elif datetime_object.hour==22:
                        weather_container[current_date]["Forecast_for_day"]["22:00"] = [str(round(temp))+"°C", weather_code_decode[code][0]+" "+weather_code_decode[code][1]]
        # print(weather_container)

        for temp_min, temp_max, code, key in zip(weather["daily"]["temperature_2m_min"], weather["daily"]["temperature_2m_max"], weather["daily"]["weathercode"], weather_container.keys()):
            weather_container[key]["Overview"]={
                "Max_temperature":str(round(temp_max))+"°C",
                "Min_temperature":str(round(temp_min))+"°C",
                "Text":weather_code_decode[code][0]+" "+weather_code_decode[code][1],
            }

        print(weather_container)
        counter_weather_schedule_onde_day = 0
        message_holder = []
        for key, value in weather_container.items():
            if method=="basic":
                # final_message_forecast = f"{key}\n\nForecast for {location} 💼:\nToday weather is: {weather_container[key]['Overview']['Max_temperature']}/{weather_container[key]['Overview']['Min_temperature']}, {weather_container[key]['Overview']['Text'].lower()}\
                # \n\n📍 00:00: {weather_container[key]['Forecast_for_day']['00:00'][0]}, {weather_container[key]['Forecast_for_day']['00:00'][1]}\
                # \n📍 08:00: {weather_container[key]['Forecast_for_day']['08:00'][0]}, {weather_container[key]['Forecast_for_day']['08:00'][1]}\
                # \n📍 12:00: {weather_container[key]['Forecast_for_day']['12:00'][0]}, {weather_container[key]['Forecast_for_day']['12:00'][1]}\
                # \n📍 15:00: {weather_container[key]['Forecast_for_day']['15:00'][0]}, {weather_container[key]['Forecast_for_day']['15:00'][1]}\
                # \n📍 18:00: {weather_container[key]['Forecast_for_day']['18:00'][0]}, {weather_container[key]['Forecast_for_day']['18:00'][1]}\
                # \n📍 22:00: {weather_container[key]['Forecast_for_day']['22:00'][0]}, {weather_container[key]['Forecast_for_day']['22:00'][1]}\
                # \n\n Have a nice day 👍".replace("Patchy", "Occasionally")
                final_message_forecast = f"{key}\n\nForecast for {location} 💼:\nToday weather is: {weather_container[key]['Overview']['Max_temperature']}/{weather_container[key]['Overview']['Min_temperature']}, {weather_container[key]['Overview']['Text'].lower()}\
                \n\n📍 00:00: {weather_container[key]['Forecast_for_day']['00:00'][0]}, {weather_container[key]['Forecast_for_day']['00:00'][1]}\
                \n📍 08:00: {weather_container[key]['Forecast_for_day']['08:00'][0]}, {weather_container[key]['Forecast_for_day']['08:00'][1]}\
                \n📍 12:00: {weather_container[key]['Forecast_for_day']['12:00'][0]}, {weather_container[key]['Forecast_for_day']['12:00'][1]}\
                \n📍 15:00: {weather_container[key]['Forecast_for_day']['15:00'][0]}, {weather_container[key]['Forecast_for_day']['15:00'][1]}\
                \n📍 18:00: {weather_container[key]['Forecast_for_day']['18:00'][0]}, {weather_container[key]['Forecast_for_day']['18:00'][1]}\
                \n\n Have a nice day 👍".replace("Patchy", "Occasionally")
                message_holder.append(translate_current_text(final_message_forecast, lang_to=user.lang, lang_from="en"))
            elif method=="manual" and counter_weather_schedule_onde_day==0:
                print(key, value)
                # final_message_forecast = f"{key}\n\nForecast for {location} 💼:\nToday weather is: {weather_container[key]['Overview']['Max_temperature']}/{weather_container[key]['Overview']['Min_temperature']}, {weather_container[key]['Overview']['Text'].lower()}\
                # \n\n📍 00:00: {weather_container[key]['Forecast_for_day']['00:00'][0]}, {weather_container[key]['Forecast_for_day']['00:00'][1]}\
                # \n📍 08:00: {weather_container[key]['Forecast_for_day']['08:00'][0]}, {weather_container[key]['Forecast_for_day']['08:00'][1]}\
                # \n📍 12:00: {weather_container[key]['Forecast_for_day']['12:00'][0]}, {weather_container[key]['Forecast_for_day']['12:00'][1]}\
                # \n📍 15:00: {weather_container[key]['Forecast_for_day']['15:00'][0]}, {weather_container[key]['Forecast_for_day']['15:00'][1]}\
                # \n📍 18:00: {weather_container[key]['Forecast_for_day']['18:00'][0]}, {weather_container[key]['Forecast_for_day']['18:00'][1]}\
                # \n📍 22:00: {weather_container[key]['Forecast_for_day']['22:00'][0]}, {weather_container[key]['Forecast_for_day']['22:00'][1]}\
                # \n\n Have a nice day 👍".replace("Patchy", "Occasionally")
                final_message_forecast = f"{key}\n\nForecast for {location} 💼:\nToday weather is: {weather_container[key]['Overview']['Max_temperature']}/{weather_container[key]['Overview']['Min_temperature']}, {weather_container[key]['Overview']['Text'].lower()}\
                \n\n📍 00:00: {weather_container[key]['Forecast_for_day']['00:00'][0]}, {weather_container[key]['Forecast_for_day']['00:00'][1]}\
                \n📍 08:00: {weather_container[key]['Forecast_for_day']['08:00'][0]}, {weather_container[key]['Forecast_for_day']['08:00'][1]}\
                \n📍 12:00: {weather_container[key]['Forecast_for_day']['12:00'][0]}, {weather_container[key]['Forecast_for_day']['12:00'][1]}\
                \n📍 15:00: {weather_container[key]['Forecast_for_day']['15:00'][0]}, {weather_container[key]['Forecast_for_day']['15:00'][1]}\
                \n📍 18:00: {weather_container[key]['Forecast_for_day']['18:00'][0]}, {weather_container[key]['Forecast_for_day']['18:00'][1]}\
                \n\n Have a nice day 👍".replace("Patchy", "Occasionally")
                counter_weather_schedule_onde_day+=1
                message_holder.append(translate_current_text(final_message_forecast, lang_to=user["Lang"], lang_from="en"))
        return message_holder
    except Exception as ex:
        print("weather_main() ",ex)
        return False

    
