# Author: <Chigozie Godwin>
# Student ID: <C2407247>


"""Importing of various dependences for the phase 2"""

import sqlite3
import sys #for ctrl c system interuption
from colorama import Fore, Style #for styling


# import matplotlib.container as container
import matplotlib.pyplot as plt
import pandas as pd

import textwrap#label
import numpy as np
from pandas.errors import EmptyDataError  # Import the EmptyDataError class

# ERROR MESSAGE STYLING
from phase_1 import WeatherApp

# Initialize the Error Styling
styling = WeatherApp('')


"""Creating of the object weather Plotter for ploting of graphs"""

class WeatherPlotter:
    def __init__(self, connection):
        self.connection = connection    
        self.exit_flag = False  # Added exit flag
    
    def plot_seven_day_precipitation(self, start_date):  

        """Plot bar chart for seven days precipitation"""  
        try:
            # Construct the SQL query
            query = """ SELECT 
                            c.name AS City,
                            dwe.date AS Date, 
                            dwe.precipitation AS Precipitation
                        FROM 
                            daily_weather_entries AS dwe
                        JOIN 
                            cities AS c ON c.id = dwe.city_id
                        WHERE                              
                            dwe.date BETWEEN ? AND DATE(?,'+6 days')
                        GROUP BY 
                            City, Date
                        ORDER BY 
                            Date;                
                    """
            # Execute the SQL query
            data = pd.read_sql_query(query, self.connection,  params=(start_date, start_date,))
                    
            # Checking if dataframe is empty
            if data.empty:

                # Using the Error styling method from phase_1 Object WeatherApp
                error_message =  f"No available data for the date: {start_date}"

                # Styling of error message
                styling.error_styling(error_message)

            else:
                # Set a larger figure size to accommodate longer labels
                plt.figure(figsize=(10, 5))
                
                # Wrap the long labels using textwrap
                wrapped_labels = [textwrap.fill(label, width=20) for label in data['City']]

                # Ploting the bar chart
                plt.bar(wrapped_labels, data['Precipitation']) 

                # Rotate the date labels to be vertical
                plt.xticks(rotation=45) 

                # Label
                plt.xlabel('City')
                plt.ylabel('Precipitation')

                # Title
                plt.title(f'7-day Precipitation for Date: {start_date} - {data["Date"].iloc[-1]} ')
                
                # Adjust layout for better appearance
                plt.tight_layout()  
                
                # Show Graph
                plt.show()

        except EmptyDataError:           
            # Using the Error styling method from phase_1 Object WeatherApp
            error_message =  f"No available data for the date: {start_date}"
            
            # Styling
            styling.error_styling(error_message)

        except Exception as e:            
            error_message = f'An error occurred: {e}'
            # Styling
            styling.error_styling(error_message)       

    
    def plot_7_day_precipitation_by_city(self, city, start_date):   

        """Query 7-day precipitation for a specific town/city"""
        try:
            # Construct the SQL query
            query = """ SELECT 
                            c.name AS City,
                            dwe.date AS Date, 
                            dwe.precipitation AS Precipitation
                        FROM 
                            daily_weather_entries AS dwe
                        JOIN 
                            cities AS c ON c.id = dwe.city_id
                        WHERE 
                            City = ?
                            AND 
                                dwe.date BETWEEN ? AND DATE(?,'+6 days')
                        LIMIT 7;                
                    """
            # Execute the SQL query
            data = pd.read_sql_query(query, self.connection,  params=(city, start_date,start_date,))
            
            # Check if the DataFrame is empty
            if data.empty:

                # Using the Error styling method from phase_1 Object WeatherApp
                error_message =  f"No available data for the date: {start_date} and City: {city}."
                
                # Styling
                styling.error_styling(error_message)
            
            else:

                # Set a larger figure size to accommodate longer labels
                plt.figure(figsize=(10, 5))
                
                # Wrap the long labels using textwrap
                wrapped_labels = [textwrap.fill(label, width=20) for label in data['Date']]  

                plt.bar(wrapped_labels, data['Precipitation'])            
                
                # Rotate the date labels to be vertical
                plt.xticks(rotation=45) 

                # Label
                plt.xlabel('Date')
                plt.ylabel('Precipitation')

                # title
                plt.title(f'7-day Precipitation for City: {city} and Date: {data["Date"].iloc[0]} - {data["Date"].iloc[6]} ')
                                
                # Adjust layout for better appearance
                plt.tight_layout()  
                
                # Show Graph
                plt.show()
        except EmptyDataError:           
            # Using the Error styling method from phase_1 Object WeatherApp
            error_message =  f"No available data for the date: {start_date} and City: {city}."
            
            # Styling
            styling.error_styling(error_message)

        except Exception as e:            
            error_message = f'An error occurred: {e}'
            # Styling
            styling.error_styling(error_message)

    
    
    def plot_precipitation_for_cities(self, cities, start_date, end_date):

        """Bar chart for a specified period for 
                a specified set of towns/cities"""
        try:
            # Ensure cities is a list, even if a single city is provided
            if not isinstance(cities, list):
                cities = [cities]

            # Sanitize city names to prevent SQL injection
            sanitized_cities = [str(city).replace("'", "''") for city in cities]

            # Create placeholders for the SQL query
            placeholders = ', '.join(['?'] * len(cities))

            # Construct the SQL query
            query = f"""
                        SELECT 
                            dwe.date AS date,
                            c.name AS city,
                            dwe.precipitation AS precipitation 
                        FROM 
                            daily_weather_entries AS dwe 
                        JOIN 
                            cities AS c ON c.id = dwe.city_id
                        WHERE 
                            c.name IN ({placeholders}) 
                            AND 
                            dwe.date                         
                            BETWEEN ? AND ?
                        GROUP BY 
                            dwe.date, c.name
                        LIMIT 20;
                    """

            # Pass parameters as a flat tuple
            params = tuple(sanitized_cities) + (start_date, end_date,)

            # Execute the SQL query
            data = pd.read_sql_query(query, self.connection, params=params)

            # Checking for empty dataframe
            if data.empty:

                # display error
                error_message = "No data available for the specified cities and date range."
                styling.error_styling(error_message)

            else:

                # Set a larger figure size to accommodate longer labels
                plt.figure(figsize=(10, 5))

                # Wrap the long labels using textwrap
                wrapped_labels = [textwrap.fill(label, width=10) for label in data['date']]

                # Adjust rotation angle and alignment
                plt.xticks(rotation=45, ha='right')  

                # Use matplotlib to plot the data
                if len(cities) == 1:

                    # Single city, use a single bar chart
                    plt.bar(wrapped_labels, data['precipitation'], label=f'{data["city"].iloc[0]}', color='skyblue')
                
                else:

                    # Multiple cities, use a grouped bar chart with different colors
                    grouped_data = data.groupby(['date', 'city'])['precipitation'].sum().unstack('city')
                    
                    # Fill missing values with 0
                    grouped_data = grouped_data.fillna(0)
                    
                    # Width of each bar
                    width = 0.2  
                    offset = -width * len(grouped_data) / 2  # Initial offset to shift bars for different cities

                    # Now, you can plot each city's data
                    for city in grouped_data.columns:
                        plt.bar(grouped_data.index, grouped_data[city], label=city)
                    
                    # Setting Legends
                    plt.legend(title='Cities')

                # Label
                plt.xlabel('Date')
                plt.ylabel('Precipitation')

                # Title
                plt.title(f'Precipitation for Cities: {", ".join(cities)}')
                
                # Adjust layout to prevent clipping
                plt.tight_layout()

                # show
                plt.show()
        
        except EmptyDataError:           
            # Using the Error styling method from phase_1 Object WeatherApp
            error_message =  "No data available for the specified cities and date range."
            
            # Styling
            styling.error_styling(error_message)

        except Exception as e:            
            error_message = f'An error occurred: {e}'
            # Styling
            styling.error_styling(error_message)

    

    def plot_avg_yearly_precipitation_by_country(self):

        """Bar chart that shows the average 
            yearly precipitation by country"""
        try:
            query = """SELECT 
                            strftime('%Y', dwe.date) as year, 
                            co.name AS country, 
                            AVG(dwe.precipitation) as avg_precipitation                     
                        FROM 
                            daily_weather_entries AS dwe
                        JOIN    
                            cities AS c ON c.id = dwe.city_id
                        JOIN    
                            countries AS co ON co.id = c.country_id  
                        GROUP BY 
                            year, country
                    """
            
            data = pd.read_sql_query(query, self.connection) 

            if data.empty:

                # display error
                error_message = "No data available."
                styling.error_styling(error_message)

            else: 

                # Set a larger figure size to accommodate longer labels
                plt.figure(figsize=(8, 4))

                # Wrap the long labels using textwrap
                wrapped_labels = [textwrap.fill(label, width=10) for label in data['year'] + ' - ' + data['country']]  

                # creating bars
                plt.bar(wrapped_labels, data['avg_precipitation'])

                # Rotate the x-axis and center the labels
                plt.xticks(rotation=45, ha='center') 

                # Increase label padding for better visibility 
                plt.xlabel('Year - Country', labelpad=15)  
                plt.ylabel('Average Precipitation')

                # Title
                plt.title('Average Yearly Precipitation by Country')

                # Adjust layout to prevent clipping
                plt.tight_layout()  

                # show
                plt.show()
        except EmptyDataError:           
            # Using the Error styling method from phase_1 Object WeatherApp
            error_message =  "No data available"
            
            # Styling
            styling.error_styling(error_message)

        except Exception as e:            
            error_message = f'An error occurred: {e}'
            # Styling
            styling.error_styling(error_message)

    def plot_grouped_bar_charts(self, selected_locations):

        """ Grouped bar charts for displaying the min/max/mean 
                temperature and precipitation 
                values for selected cities or countries """
        try: 
            # Use triple-quoted string for better readability
            query = f"""
                SELECT
                    c.name AS location,
                    dwe.min_temp AS min_temp,
                    dwe.max_temp AS max_temp,
                    dwe.mean_temp AS mean_temp,
                    AVG(precipitation) as mean_precipitation
                FROM
                    daily_weather_entries as dwe
                JOIN
                    cities AS c ON c.id = dwe.city_id
                WHERE
                    location IN ({','.join(['?']*len(selected_locations))})
                GROUP BY
                    location
            """

            
            data = pd.read_sql_query(query,  self.connection, params=tuple(selected_locations))

            if data.empty:
                # Using the Error styling method from phase_1 Object WeatherApp
                error_message =  f"No data available for the specified location(s): {selected_locations}."
                
                # Styling
                styling.error_styling(error_message)
            else:
                # Set the location names as index
                # Reset the index after setting it to 'location'
                # data.reset_index(inplace=True)
                data.set_index('location', inplace=True)

                # Setting a larger figure size to accommodate longer labels
                plt.figure(figsize=(12, 8))

                # Plot the grouped bar chart
                ax = data[['min_temp', 'max_temp', 'mean_temp', 'mean_precipitation']].plot(kind='bar', stacked=False, ax=plt.gca(), alpha=0.7)
                wrapped_labels = data.index.tolist()
                
                # Set x-axis ticks and labels
                ax.set_xticks(range(len(data)))
                ax.set_xticklabels(wrapped_labels, rotation=45, ha='right')

                # Set axis labels 
                plt.xlabel('Location')
                plt.ylabel('Values')

                # title
                plt.title(f'Weathertrends for {", ".join(selected_locations)}')

                # Use legend for better clarity
                plt.legend()

                # Ensure a tight layout for better visualization
                plt.tight_layout()

                # Manually adjust subplot parameters
                plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

                # Display the plot
                plt.show()

        except EmptyDataError:           
            # Using the Error styling method from phase_1 Object WeatherApp
            error_message =  f"No data available for the specified location(s): {selected_locations}."
            
            # Styling
            styling.error_styling(error_message)

        except Exception as e:            
            error_message = f'An error occurred: {e}'
            # Styling
            styling.error_styling(error_message)
    
    def plot_daily_temperature_for_month( self, city, year, month):

        """Multi-line chart for daily min/max temperature for a 
                                    given month for a specific city"""
    
        # SQL query to retrieve daily temperature data for the specified city
        try:
            query = """SELECT 
                            dwe.date AS date,
                            dwe.min_temp AS min_temperature,
                            dwe.max_temp AS max_temperature
                        FROM 
                            daily_weather_entries AS dwe
                        JOIN 
                            cities AS c ON c.id = dwe.city_id
                        WHERE 
                            c.name = ? 
                        AND 
                            strftime('%Y-%m', dwe.date) = ?;
                    """
            
            # Execute the query and fetch data using pandas
            data = pd.read_sql_query(query, self.connection,   params=(city, f"{year}-{month:02d}"))

            if data.empty:
                # display error
                error_message = f"No data available for the specified {city}, {year} and {month}."
                styling.error_styling(error_message)
            else:
                # Set a larger figure size to accommodate longer labels
                plt.figure(figsize=(10, 7))

                # Wrap the long labels using textwrap
                wrapped_labels = [textwrap.fill(label, width=10) for label in data['date']]  

                # Rotate the x-axis and center the labels
                plt.xticks(rotation=45, ha='center')  
                
                # Plot lines for min and max temperatures
                # Plot multiline chart
                plt.plot(wrapped_labels, data['min_temperature'], label='Min Temperature')
                plt.plot(wrapped_labels, data['max_temperature'], label='Max Temperature')
                
                # Set axis labels and plot title
                plt.xlabel('Date')
                plt.ylabel('Temperature')
                plt.title(f'Daily Min/Max Temperature for {city} - {year}-{month:02d}')
                
                # Display legend
                plt.legend()
                
                # Ensure a tight layout for better visualization
                plt.tight_layout()
                
                # Show the plot
                plt.show()
        
        except EmptyDataError:           
            # Using the Error styling method from phase_1 Object WeatherApp
            error_message =  f"No data available for the specified {city}, {year} and {month}."
            
            # Styling
            styling.error_styling(error_message)

        except Exception as e:            
            error_message = f'An error occurred: {e}'
            # Styling
            styling.error_styling(error_message)
    
    
    def plot_scatter_avg_temp_vs_rainfall(self, locations):

        """Scatter plot chart for average temperature against average rainfall 
                        for town/city/country/all countries etc"""        
        
        try:
            if isinstance(locations, str):
                # Convert single location to a list for consistency
                locations = [locations]

            for location in locations:
                query = """SELECT c.name AS city, 
                                dwe.mean_temp as avg_temperature, 
                                dwe.precipitation as avg_precipitation 
                            FROM 
                                daily_weather_entries AS dwe 
                            JOIN
                                cities AS c ON c.id = dwe.city_id
                            WHERE 
                                city = ?
                        """

                # Execute the query with the specified location parameter
                data = pd.read_sql_query(query, self.connection, params=(location,))

                if not data.empty:

                    # Generate scatter plot if data is not empty
                    x = data['avg_temperature']
                    y = data['avg_precipitation']
                    plt.scatter(x, y, label='Data Points')

                    # Fit a linear trendline (polynomial of degree 1)
                    coefficients = np.polyfit(x, y, 1)
                    trendline = np.poly1d(coefficients)
                    plt.plot(x, trendline(x), color='red', label='Trendline')

                    # Label
                    plt.xlabel('Average Temperature')
                    plt.ylabel('Average Precipitation')
                    
                    # Title
                    plt.title(f'Scatter Plot: Average Temperature vs. Average Precipitation - {location}')
                    
                    # Show
                    plt.show()
                else:                   

                    # Using the Error styling method from phase_1 Object WeatherApp
                    error_message =  f"No data found for {location}. Note: You can only check for one location at a time."
            
                    # Styling
                    styling.error_styling(error_message)

        except EmptyDataError:           

            # Using the Error styling method from phase_1 Object WeatherApp
            error_message =  f"No data found for {location}. Note: You can only check for one location at a time."
            
            # Styling
            styling.error_styling(error_message)

        except Exception as e:            

            error_message = f'An error occurred: {e}'

            # Styling
            styling.error_styling(error_message)

    def is_valid_choice(self, choice):
        return choice.lower() == 'x' or (choice.isdigit() and 1 <= int(choice) <= 7)
    
    def choose_option(self):
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'SELECT AN OPTIONS:'}{Style.RESET_ALL}")   
             
        print("1. Plots seven-day precipitation data.")
        print("2. Plots seven-day precipitation data for a specific city.")
        print("3. Plots precipitation data for multiple cities within a date range.")
        print("4. Plots average yearly precipitation data by country.")
        print("5. Bar charts for selected locations.")
        print("6. Plots daily temperature data for a specific city and month.")
        print("7. Plots scatter plot comparing average temperature and rainfall for multiple locations.")           
        print(f"{Fore.RED}{Style.BRIGHT}{'x. Quit'}{Style.RESET_ALL}")

        print(f'{Fore.YELLOW}{Style.BRIGHT}{"-"*100}{Style.RESET_ALL}')
        
        try: 
            choice = input('Enter your choice (1-7 To see chart or X to Quit): ')
            print(f'{Fore.YELLOW}{Style.BRIGHT}{"-"*100}{Style.RESET_ALL}')

            if not choice.lower() == 'x' and (not choice.isdigit() or int(choice) < 1 or int(choice) > 7):

                raise ValueError(f"Invalid input {choice}. Please enter a number between 1 and 7 or X.")
            
            return choice
        
        except ValueError as ve:
                
                styling.error_styling(f"Invalid input: {ve}")     

               
    
    def phaseTwoMenu(self):

        # Options that correspond to each choice
        options = {
                    '1': 'Plots seven-day precipitation data.',
                    '2': 'Plots seven-day precipitation data for a specific city.',
                    '3': 'Plots precipitation data for multiple cities within a date range.',
                    '4': 'Plots average yearly precipitation data by country.',
                    '5': 'Bar charts for selected locations.',
                    '6': 'Plots daily temperature data for a specific city and month.',
                    '7': 'Plots scatter plot comparing average temperature and rainfall for multiple locations.',
                    "x": "Quit"
                }

        '''changed from one choice option to another'''

        while True: 
            
            try:                
                choice = self.choose_option()
                
                # if choice is None:
                #     continue
                                                
                if choice in options:
                    
                    # Get the required parameters from the user                    
                        
                    if choice == "1":
                        Start_Date = input('Enter Start Date (YYYY-MM-DD): ')
                        self.plot_seven_day_precipitation(Start_Date)                                    
                        
                    elif choice == "2":
                        
                        Start_Date = input('Enter Start Date (YYYY-MM-DD): ')
                        City = input('Enter Name of City: ')
                        self.plot_7_day_precipitation_by_city(City, Start_Date) 
                                            
                    elif choice == "3":
                        # Collect user input
                        start_date = input("Enter start date (YYYY-MM-DD): ")
                        end_date = input("Enter end date (YYYY-MM-DD): ")
                        city_input = input("Enter city or cities (comma-separated): ")
                        cities = city_input.split(',')
                        self.plot_precipitation_for_cities(cities, start_date, end_date) 

                    elif choice == "4":                    
                        self.plot_avg_yearly_precipitation_by_country()
                    
                    elif choice == "5":
                        user_input = input("Enter the locations separated by commas: ")

                        # Split the input string into a list of locations
                        selected_locations = [location.strip() for location in user_input.split(',')]
                        
                        self.plot_grouped_bar_charts(selected_locations)
                    
                    elif choice == "6":
                        city    =   input('Enter City: ')
                        year    =   int(input('Enter Year (YYYY): '))
                        month   =   int(input('Enter Month (MM): '))
                        self.plot_daily_temperature_for_month(city, year, month)
                    
                    elif choice == "7":
                        location = input('Enter A City Name: ')
                        self.plot_scatter_avg_temp_vs_rainfall(location)
                    
                    elif choice.lower() == "x":
                        x = ['buy...']
                        styling.style_output(x)
                        break

                    else:
                        x = f'Invalid choice: {choice}. Please enter a valid option.'
                        styling.error_styling(x)
                    
            except KeyboardInterrupt:
                # Handle Ctrl+C, perform cleanup, and exit gracefully
                print("Ctrl+C pressed. Quiting...")
                sys.exit(0)  

                       

if __name__ == "__main__":
              
    # Handle database connection errors
    try:
        # Database path
        path = 'db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db'
        # Create a SQLite3 connection and call the various functions
        with sqlite3.connect(path) as db:
            wp = WeatherPlotter(db)
            wp.phaseTwoMenu()
    except sqlite3.Error as e:
        styling.error_styling(f"Database connection error: {e}")
        sys.exit(1)  # Exit with error code 1
    except Exception as e:
        styling.error_styling(f"An unexpected error occurred: {e}")
        sys.exit(1)  # Exit with error code 1
