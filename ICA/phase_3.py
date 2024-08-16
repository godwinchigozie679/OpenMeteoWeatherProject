# Author: <Chigozie Godwin>
# Student ID: <C2407247>


from phase_1 import WeatherApp
from phase_2 import WeatherPlotter
from phase_4 import AddOrUpdateWeatherAppData
import sqlite3

# MESSAGE STYLING
from phase_1 import WeatherApp

# Initialize the Styling
styling = WeatherApp('')

"""
Class to delete by city, country, or specific time period
"""
class DeleteWeatherAppData:

    def __init__(self, connection):
        self.connection = connection
    
    
    # validate data
    def delete_data(self, city_name, country_name, start_date, end_date):
        try:
            cursor = self.connection.cursor()

            # Get Country_id
            country_data = cursor.execute('SELECT id FROM countries WHERE name = ?', (country_name,)).fetchone()
            
            if country_data is not None:
                country_id  = country_data[0]                 

                # Get City_id
                city_data = cursor.execute('SELECT id FROM cities WHERE name = ? AND country_id = ?', (city_name, country_id)).fetchone()
                
                if city_data is not None:
                    city_id  = city_data[0]                     

                    params = (city_id, start_date, end_date)

                    # Check if entries exist in daily_weather_entries within the date range        
                    if start_date == end_date:
                        data = cursor.execute('SELECT * FROM daily_weather_entries WHERE city_id = ? AND date BETWEEN ? AND ?', 
                                params)
                        # get single data for validation
                        data_exist = data.fetchone()
                        
                        if data_exist:
                            cursor.execute('DELETE FROM daily_weather_entries WHERE city_id = ? AND date BETWEEN ? AND ?', 
                            # Delete entries from daily_weather_entries for the specified city, country, and date range
                                        params)
                            self.connection.commit()
                            # Success message
                            message = [f"Daily weather entries deleted for City: {city_name}, Country: {country_name}, and Date: {start_date}"]

                            styling.style_output(message)
                            # Check if any remaining entries for the same city or country in daily_weather_entries
                            cursor.execute('SELECT * FROM daily_weather_entries WHERE city_id = ?', (city_id,))
                            remaining_entries = cursor.fetchone()
                            if not remaining_entries:
                                # No remaining entries, delete from cities and countries tables
                                cursor.execute('DELETE FROM cities WHERE id = ?', (city_id,))
                                cursor.execute('DELETE FROM countries WHERE id = ?', (country_id,))
                                self.connection.commit()
                            else:
                                # Success message
                                message = f"No entries found for City: {city_name}, Country: {country_name}, within Date: {start_date} in daily weather entries"
                                styling.error_styling(message)
                        else:
                            message = f"No entries found for City: {city_name}, Country: {country_name}, within Date: {start_date} in daily weather entries"
                            
                            styling.error_styling(message)
                    
                    else:
                        data = cursor.execute('SELECT * FROM daily_weather_entries WHERE city_id = ? AND date BETWEEN ? AND ?', 
                                params).fetchall()  

                        if data:
                            # Extract unique IDs from the data list
                            entry_ids = [entry[0] for entry in data]
                            print(entry_ids)
                            # Delete entries from daily_weather_entries for the specified IDs
                            cursor.execute(f'DELETE FROM daily_weather_entries WHERE id IN ({",".join(["?"] * len(entry_ids))})', entry_ids)

                            self.connection.commit()

                            # Check if any remaining entries for the same city or country in daily_weather_entries
                            cursor.execute('SELECT * FROM daily_weather_entries WHERE city_id = ?', (city_id,))
                            remaining_entries = cursor.fetchone()

                            if not remaining_entries:
                                # No remaining entries, delete from cities and countries tables
                                cursor.execute('DELETE FROM cities WHERE id = ?', (city_id,))
                                cursor.execute('DELETE FROM countries WHERE id = ?', (country_id,))
                                self.connection.commit()

                            # Success message
                            message = [f"Daily weather entries deleted for City: {city_name}, Country: {country_name}, and \nDate Range: {start_date} to {end_date}"]

                            styling.style_output(message)

                        else:
                            # No entries found
                            message = f"No entries found for City: {city_name}, Country: {country_name}, within \nDate Range: {start_date} to {end_date} in daily weather entries"
                            styling.error_styling(message)
                else:
                   message = (f"City with name {city_name} for country: {country_name} not found.")
                   styling.error_styling(message)
            
            else:
                message = (f"Country with name {country_name} not found.")  
                styling.error_styling(message)

        except sqlite3.Error as e:
            print(f"Error: {e}")
        
    def phaseThreeMenu(self):

        try:
            print("Data to delete>>>>>: ")
            country_name    =   input("What country? (Capitalize: A-z): ").capitalize()
            city_name       =   input("What city? (Capitalize: A-z): ").capitalize()
            start_date      =   input("From what date? (YYYY-MM-DD): ") 
            end_date        =   input("to what date? (YYYY-MM-DD): ")

            self.delete_data(city_name, country_name, start_date, end_date)
        except:
            message = f"You inputed the wrong information!"
            styling.error_styling(message)

def phaseThreeMenu():
     while True:
            # Display menu options
            print("Select a phase:")
            print("1. Phase 1")
            print("2. Phase 2")
            print("3. Phase 3")
            print("4. Phase 4")
            print("5. Exit")

            # Get user choice
            user_choice = input("Enter the number of the phase you want to view: ")

            if user_choice == '1':
                weather_app.phaseOneMenu()
            elif user_choice == '2':
                weather_plotter.phaseTwoMenu()
            elif user_choice == '3':
                delete_weather_data.phaseThreeMenu()
            elif user_choice == '4':
                add_or_update_weather_app.phaseFourMenu()
            elif user_choice == '5':
                print("Exiting the weather application. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

            # Ask the user if they want to continue
            user_input = input("Do you want to view another phase? (yes/no): ").lower()

            if user_input != 'yes':
                message = ["Exiting the weather application. Goodbye!"]
                styling.style_output(message)
                break



if __name__ == "__main__":
    db_path = 'db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db'
    
    with sqlite3.connect(db_path) as db:
        #Initialize Weatherapp class
        weather_app = WeatherApp(db)       
        weather_plotter = WeatherPlotter(db)
        delete_weather_data = DeleteWeatherAppData(db)
        add_or_update_weather_app = AddOrUpdateWeatherAppData(db)

        phaseThreeMenu()