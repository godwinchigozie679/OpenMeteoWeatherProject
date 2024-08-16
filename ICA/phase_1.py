# Author: <Chigozie Godwin>
# Student ID: <C2407247>

import sqlite3
from colorama import Fore, Style
import sys #for ctrl c system interuption





# Phase 1 - Starter
# 
# Note: Display all real/float numbers to 2 decimal places.
class WeatherApp:
    def __init__(self, connection):
        self.connection = connection

    def style_output(self, output):
        
        """Variables created for styling output"""
        output_header = f'{Fore.CYAN}{Style.BRIGHT}{"*"*46}{Style.RESET_ALL}'
        output_title = f"{Fore.GREEN}{Style.BRIGHT}{' OUTPUT '}{Style.RESET_ALL}"
        output_footer = f'{Fore.CYAN}{Style.BRIGHT}{"*"*46}{Style.RESET_ALL}'
        
        # Print the header, title, and footer
        print(f'{output_header}{output_title}{output_footer}')
        
        # Print the contents of the output variable
        
        try:
            
            if len(output) > 1:
                for data in output:
                    print(data)
            else:
                print(output[0])
        except:
            pass

        # Print the additional line of asterisks
        print(f"{Fore.CYAN}{Style.BRIGHT}{'*'*100}{Style.RESET_ALL}") 
        
    
    def error_styling(self, error_message):

        """Variables created for styling output"""
        output_header = f'{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{"*"*46}{Style.RESET_ALL}'
        output_title = f"{Fore.YELLOW}{Style.BRIGHT}{' ERROR  '}{Style.RESET_ALL}"
        output_footer = f'{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{"*"*46}{Style.RESET_ALL}'

        # Print the header, title, and footer
        print(f'{output_header}{ output_title }{output_footer}')

        # Print the contents of the output variable

        print(f"{Fore.RED}{Style.BRIGHT}{error_message}{Style.RESET_ALL}")
        

        # Print the additional line of asterisks
        print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{'*'*100}{Style.RESET_ALL}")
    
    '''
    Satisfactory
    '''

    def select_all_countries(self):
        # Queries the database and selects all the countries 
        # stored in the countries table of the database.
        # The returned results are then printed to the 
        # console.
        try:
            # Define the query
            query = """ 
                        SELECT * 
                        FROM [countries]
                    """
            # 
            self.connection.row_factory = sqlite3.Row
            
            # Get a cursor object from the database connection
            # that will be used to execute database query.
            cursor = self.connection.cursor()

            # Execute the query via the cursor object.
            results = cursor.execute(query)

            # Collect results in a list and return it
            data = []
            # Iterate over the results and display the results.
            for row in results:

                data.append(f"Country Id: {row['id']} -- Country Name: {row['name']} -- Country Timezone: {row['timezone']}")

            return data
        
        except sqlite3.OperationalError as ex:
            print(ex)
            # Return an empty list in case of an error
            return []

    def select_all_cities(self):
        
        try:
            query = """ SELECT *        
                        FROM   
                        [cities]              
                    """
            
            # 
            self.connection.row_factory = sqlite3.Row

            # that will be used to execute database query.
            cursor = self.connection.cursor()

            
            # Execute the query via the cursor object.
            results = cursor.execute(query)
            
            # Collect results in a list and return it
            data = []
            
            # Iterate over the results and display the results.
            for row in results:
                data.append(f"City Id: {row['id']} -- City Name: {row['name']} -- City Latitude: {row['latitude']} ---- -- Country Longitude: {row['longitude']}")
            
            return data
        
        except sqlite3.OperationalError as ex:
            print(ex)

    '''
    Good
    '''
    def average_annual_temperature(self, city_id, year):
        try:
            query = '''
                        SELECT AVG(mean_temp) 
                            AS avg_annual_temperature
                        FROM 
                            daily_weather_entries
                        WHERE 
                            city_id = ?
                            AND strftime('%Y', date) = ?
                    '''
            self.connection.row_factory = sqlite3.Row
            
            # This will be used to execute database query.
            cursor = self.connection.cursor()
            
            # Execute the query via the cursor object.
                
            result = cursor.execute(query, (city_id, year))

            # Fetch the result
            result = result.fetchone()

            # Collect results in a list and return it
            data = []

            try:
                if result:
                    temperature = result['avg_annual_temperature']
                    data.append(f"City ID: {city_id} -- Year: {year} -- Average Annual Temperature: {temperature:.2f} Degree Celsius")
                    
                
                else:
                    error_message = f"No results found for City ID: {city_id} in the year {year}."
                    self.error_styling(error_message)                   
                
                return data
                
            except TypeError:
                error_message = f"Invalid input, City ID: {city_id} in the year {year}. Please enter a valid City ID and Year."
                self.error_styling(error_message)

        except sqlite3.OperationalError as ex:
            error_message = f"Error in average_annual_temperature: {ex}"
            self.error_styling(error_message)
            

    ''''''
    def average_seven_day_precipitation(self, city_id, start_date):
        # TODO: Implement this function
        try:
            query = """
                        SELECT 
                            AVG(precipitation) AS avg_seven_precipitation
                        FROM 
                            daily_weather_entries
                        WHERE 
                            city_id = ?
                        AND 
                            date >= ?
                        LIMIT 7;
                    """
            
            self.connection.row_factory = sqlite3.Row
            # that will be used to execute database query.
            cursor = self.connection.cursor()
            
            # Execute the query via the cursor object.
            results = cursor.execute(query, (city_id, str(start_date)))

            # Fetch the result
            result = results.fetchone()

            # Collect results in a list and return it
            data = []
            
            # Display the result
            if result and result['avg_seven_precipitation'] is not None:
                data.append(f"City Id: {city_id} -- Average Seven Day Precipitation: {result['avg_seven_precipitation']:.2f}")
            else:
                error_message = f"No results found."
                self.error_styling(error_message)

            return data


        except sqlite3.OperationalError as ex:
            error_message = f"{ex}"
            self.error_styling(error_message)


    '''
    Very good
    '''
    def average_mean_temp_by_city(self, date_from, date_to):
        try:
            query = """ SELECT 
                            c.name AS City, 
                            AVG(dwe.mean_temp) AS Avg_mean_temperature
                        FROM 
                            daily_weather_entries as dwe
                            JOIN cities AS c ON dwe.city_id = c.id
                        WHERE 
                            date 
                        BETWEEN 
                            ? AND ?
                        GROUP BY 
                            c.name; 
                    """

            self.connection.row_factory = sqlite3.Row

            cursor = self.connection.cursor()

            #Execute the query via the cursor object.
            results = cursor.execute(query, (str(date_from), str(date_to)))

            # Fetch the results
            result_rows = results.fetchall()

            # Collect results in a list and return it
            data = []

            # Display the results
            if result_rows:
                print("Average Mean Temperature by City:")
                for row in result_rows:
                    city_name = row['City']
                    avg_temp = row['Avg_mean_temperature']
                    data.append(f"{city_name}: {avg_temp:.2f}°C") 
                return data               
            else:
                error_message = "No results found."
                self.error_styling(error_message)
            
            return data

        except sqlite3.OperationalError as ex:
            error_message = f"{ex}"
            self.error_styling(error_message)


    def average_annual_precipitation_by_country(self, year):

        try:
            query = """ SELECT  
                            co.name AS Country_name, 
                            AVG(dwe.precipitation) AS Avg_annual_precipitation
                        FROM    
                            daily_weather_entries AS dwe
                        JOIN    
                            cities AS c ON c.id = dwe.city_id
                        JOIN    
                            countries AS co ON co.id = c.country_id    
                        WHERE 
                            strftime('%Y', date) = ?
                        GROUP BY 
                            Country_name; 
                """
            
            self.connection.row_factory = sqlite3.Row
            cursor = self.connection.cursor()

            results = cursor.execute(query, (year,))

            rows = results.fetchall()

            # Collect results in a list and return it
            data = []

            if rows:
                print("Average Annual Precipitation by Country:")
                for row in rows:
                    country_name = row['Country_name']
                    avg_precipitation = row['Avg_annual_precipitation']
                    data.append(f"{country_name}: {avg_precipitation:.2f} mm")
                return data
            else:
                error_message = "No results found."
                self.error_styling(error_message)
            
            return data

        except sqlite3.OperationalError as ex:
            error_message = f"{ex}"
            self.error_styling(error_message)
    '''
    Excellent

    You have gone beyond the basic requirements for this aspect.

    '''

    def choose_option(self):
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'SELECT AN OPTIONS:'}{Style.RESET_ALL}")   
             
        print("1. All Countries")
        print("2. All cities")
        print("3. Average Annual Temperature")
        print("4. Average seven day precipitation")
        print("5. Average Mean Temp by City")
        print("6. average_annual_precipitation_by_country")        
        print(f"{Fore.RED}{Style.BRIGHT}{'x. Quit'}{Style.RESET_ALL}")

        print(f'{Fore.YELLOW}{Style.BRIGHT}{"-"*100}{Style.RESET_ALL}')
        
        try: 
            choice = input('Enter your choice (0-6): ')
            print(f'{Fore.YELLOW}{Style.BRIGHT}{"-"*100}{Style.RESET_ALL}')

            if not choice.lower() == 'x' and (not choice.isdigit() or int(choice) < 0 or int(choice) > 6):
                raise ValueError(f"Invalid input {choice}. Please enter a number between 0 and 6 or X.")
            return choice
        except ValueError as ve:
                self.error_styling(f"Invalid input: {ve}")


    def phaseOneMenu(self):

        # Options that correspond to each choice
        options = {
            "1": "select_all_countries",
            "2": "select_all_cities",
            "3": "average_annual_temperature",
            "4": "average_seven_day_precipitation",
            "5": "average_mean_temp_by_city",
            "6": "average_annual_precipitation_by_country",
            "x": "Quit"
        }

        '''changed from one choice option to another'''
        while True: 
            try:
                choice = self.choose_option()
                                                
                if choice in options:
                    # Get the required parameters from the user
                    if choice == "1":
                        x = self.select_all_countries() 
                        self.style_output(x)                                    
                        
                    elif choice == "2":
                        
                        x = self.select_all_cities() 
                        self.style_output(x) 
                                            
                    elif choice == "3":
                        # Collect user input
                        city_id = int(input("Enter City ID: ")) 
                        year = input("Enter Year (YYYY): ")                        
                        
                        # Result
                        x = self.average_annual_temperature(city_id, year)                           
                        self.style_output(x) 

                    elif choice == "4":                    
                        city_id = int(input("Enter the City ID: ")) 
                        start_date = input("Enter Year (YYYY-MM-DD): ")                        
                        
                        x  = self.average_seven_day_precipitation(city_id, start_date)
                        self.style_output(x)
                    
                    elif choice == "5":
                        date_from   =   input("Enter Start Date (YYYY-MM-DD): ")
                        date_to     =   input("Enter End Date (YYYY-MM-DD): ")                        
                        
                        x = self.average_mean_temp_by_city(date_from, date_to)
                        self.style_output(x)
                    
                    elif choice == "6":
                        year = input("Enter Year (YYYY): ")                        
                        
                        x = self.average_annual_precipitation_by_country(year)
                        self.style_output(x)
                        
                    elif choice == "x": # added this option
                        x = ['bye...']
                        self.style_output(x)
                        break
                    elif choice is None:
                        continue
                    else:
                        x = f'Invalid input {choice}. Please enter a number between 0 and 6.'
                        self.error_styling(x)
            
           
            except KeyboardInterrupt:
                # Handle Ctrl+C, perform cleanup, and exit gracefully
                print("Ctrl+C pressed. Quiting...")
                sys.exit(0)  

                   

if __name__ == "__main__":
    db_path = 'db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db'
    
    with sqlite3.connect(db_path) as db:
        weather_app = WeatherApp(db)
        weather_app.phaseOneMenu()        
        
        
            
            