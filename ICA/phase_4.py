# Author: <Chigozie Godwin>
# Student ID: <C2407247>


# I use this to get the timezone of the location
from timezonefinder import TimezoneFinder

import requests

# for database query
import sqlite3


# MESSAGE STYLING
from phase_1 import WeatherApp

# Initialize the Styling
styling = WeatherApp('')

# I use this to get latitude and longitude based on user input
from geopy.geocoders import Nominatim


class AddOrUpdateWeatherAppData:
    def __init__(self, connection):
        self.connection = connection

    """Get Country, Latitude and Logitude when user type a city name.
    This details will be use in the Open-Meteo API
    """
    def get_country_lat_long_timezone(self, city):
        # Initialize a geolocator
        geolocator = Nominatim(user_agent="geo_locator")

        try:
            # Get location information (latitude, longitude, and country) with timezone
            location = geolocator.geocode(city, addressdetails=True, language="en")

            # Check if the location was found
            if location:
                # Extract country, latitude, and longitude from raw response
                raw_data = location.raw
                country = raw_data.get('address', {}).get('country', 'N/A')
                
                # round to two decimal places
                latitude = round(location.latitude, 5)
                longitude = round(location.longitude, 5)

                
                # Get the time zone based on latitude and longitude
                timezone_finder = TimezoneFinder()
                timezone = timezone_finder.timezone_at(lat=latitude, lng=longitude)
            
                return country, latitude, longitude, timezone
            else:
                print(f"Location not found for city: {city}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return country, latitude, longitude, timezone


# Collect data from meteo weather api
    def open_meteo_weather(self, city_name, country, latitude, longitude, timezone, start_date, end_date):
    
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date,
            "end_date": end_date,
            "daily": ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", "precipitation_sum"],
            "timezone": timezone
        }

        country = country        

        
        try:
            response = requests.get(url, params=params)
            data = response.json()
        except:
            x = f'Wrong Data Format'
            styling.error_styling(x)
            
        
        
        daily_weather = {
                        'date'                      :       data['daily']['time'],        
                        'max_temp'                  :       data['daily']['temperature_2m_max'],
                        'min_temp'                  :       data['daily']['temperature_2m_min'],
                        'mean_temp'                 :       data['daily']['temperature_2m_mean'],
                        'precipitation'             :       data['daily']['precipitation_sum'],    
                        "latitude"                  :       data['latitude'],
                        "longitude"                 :       data['longitude'], 
                        "country"                   :       country,
                        "cities"                    :       city_name,
                        "timezone"                  :       data["timezone"]
                    }
    
    
        return daily_weather
        

    def insert_or_update_country(self, country_name, timezone):
        
        cursor = self.connection.cursor()
        # Check if the country already exists
        cursor.execute("SELECT id FROM countries WHERE name=?", (country_name,))

        existing_country_id = cursor.fetchone()
        
        if existing_country_id:
            # Country exists, update the timezone
            country_id = existing_country_id[0]
            cursor.execute("UPDATE countries SET timezone=? WHERE id=?", (timezone, country_id))
        
            return country_id
        else:
            # Country does not exist, insert a new record
            cursor.execute("INSERT INTO countries (name, timezone) VALUES (?, ?)", (country_name, timezone))
            country_id = cursor.lastrowid

        # Commit changes
        self.connection.commit()

        return country_id    
    
    def insert_into_cities(self, cities, longitude, latitude, country_id):
        # Connect to the SQLite database (create one if not exists)
        cursor = self.connection.cursor()

        # Check if the city_id already exists in the table
        cursor.execute("SELECT id FROM cities WHERE latitude = ? AND longitude = ?", (latitude, longitude,))
        existing_data = cursor.fetchone()
        
        # cities:
        #    name, longitude, latitude, country_id
        if existing_data:
            city_id = existing_data[0]
            
            # Update the existing record
            cursor.execute("UPDATE cities SET name = ?,  longitude = ?, latitude = ?, country_id = ?  WHERE id = ?",
                        (cities, longitude, latitude, country_id, city_id,))
            
            return city_id
        else:
            # Insert a new record
            cursor.execute("INSERT INTO cities (name, longitude, latitude, country_id) VALUES (?, ?, ?, ?)",
                        (cities, longitude, latitude, country_id,))

        # Commit the changes 
        self.connection.commit()
        
        city_id = cursor.lastrowid
        
        return city_id

    def insert_or_update_daily_weather_entries(self, date, min_temp, max_temp, mean_temp, precipitation, city_id):  # Connect to the SQLite database (create one if not exists)
        cursor = self.connection.cursor()
        
        data = zip(date, min_temp, max_temp, mean_temp, precipitation, city_id)

        for item in data:
            date, min_temp, max_temp, mean_temp, precipitation, city_id = item        
            params = (date, min_temp, max_temp, mean_temp, precipitation, city_id,)

            # Check if the city_id already exists in the table
            cursor.execute("""  SELECT id 
                                FROM 
                                    daily_weather_entries 
                                WHERE 
                                    date = ? AND min_temp = ? AND max_temp = ? AND mean_temp = ? AND precipitation = ? AND city_id = ?""", 
                        params)        
            existing_data = cursor.fetchone()

            if existing_data:
                
                # Fetch city
                cursor.execute("""UPDATE daily_weather_entries 
                                    SET date = ?, min_temp = ?, max_temp = ?, mean_temp = ?, precipitation = ?, city_id = ?  
                            WHERE date = ? AND min_temp = ? AND max_temp = ? AND mean_temp = ? AND precipitation = ? AND city_id = ?""",
                            (date, min_temp, max_temp, mean_temp, precipitation, city_id, date, min_temp, max_temp, mean_temp, precipitation, city_id,))
                
            else:
                # Insert a new record
                cursor.execute("""INSERT INTO daily_weather_entries 
                            (date, min_temp, max_temp, mean_temp, precipitation, city_id) 
                            VALUES (
                            ?, ?, ?, ?, ?, ?)""",
                            params)
                
        # Commit the changes and close the connection
        self.connection.commit()
        
        message = [f"Weather data processed successfully....."]
        styling.style_output(message)

    def phaseFourMenu(self):
        try:
            # Get user city name
            city_name = input("Enter the city name to add or update: ").capitalize()

            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            
            # Getting country, latitude, longitude, and timezone from the get get_country_lat_long_timezone method
            country, latitude, longitude, timezone = self.get_country_lat_long_timezone(city_name)


            # Get weather data
        
            get_data = self.open_meteo_weather(city_name, country, latitude, longitude, timezone, start_date, end_date)
           
        
            country_name = get_data["country"]
            timezone = get_data["timezone"]

            # insert or update country
            country_id = self.insert_or_update_country(country_name, timezone)  
            
            # Insert or update city
            cities = get_data["cities"]
        
            city_id = self.insert_into_cities(cities, longitude, latitude, country_id)   
            

            """Insert or update daily weather entries"""
            # daily_weather_entries
            date            =       get_data.get('date')
            min_temp        =       get_data.get('min_temp')
            max_temp        =       get_data.get('max_temp')
            mean_temp       =       get_data.get("mean_temp")
            precipitation   =       get_data.get('precipitation')
            city_id         =       [city_id] * len(min_temp)
        
            self.insert_or_update_daily_weather_entries(date, min_temp, max_temp, mean_temp, precipitation, city_id)        
    
        except:
            x = f'Wrong Data Format'
            styling.error_styling(x) 



if __name__ == "__main__":
    db_path = 'db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db'
    
    with sqlite3.connect(db_path) as db_conn:
        x = AddOrUpdateWeatherAppData(db_conn)

        x.phaseFourMenu( )
        


        