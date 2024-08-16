# WeatherApp PHASE 1 README

## Author
- Chigozie Godwin
- Student ID: C2407247

## Overview
This Python script, WeatherApp, is designed to interact with a SQLite database containing weather-related data. It provides functionalities to query and display information about countries, cities, and weather statistics.

## Requirements
- colorama==0.4.6
- contourpy==1.2.0
- cycler==0.12.1
- fonttools==4.44.3
- greenlet==3.0.1
- kiwisolver==1.4.5
- matplotlib==3.8.2
- numpy==1.26.2
- packaging==23.2
- pandas==2.1.3
- Pillow==10.1.0
- pyparsing==3.1.1
- python-dateutil==2.8.2
- pytz==2023.3.post1
- six==1.16.0
- SQLAlchemy==2.0.23
- typing_extensions==4.8.0
- tzdata==2023.3


## Installation
1. Clone this repository to your local machine.
   ```bash
   git clone https://github.com/yourusername/WeatherApp.git

1. Navigate to the project directory.

   ```bash
   cd WeatherApp

2. Install the required Python packages.
   ```bash
   pip install -r requirements.txt

3. Create a SQLite database and update the db_path variable in the script with the correct path to your database file.

## Database Setup
The script uses an SQLite database located at db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db.

## Usage
Run the WeatherApp script using the following command:

1. Navigate to the project directory.

   ```bash
   python phase_1.py
or anything you rename the .py file

Follow the on-screen prompts to select different options and retrieve weather-related information.

## Options
The script provides the following options:

1. Display all countries.
2. Display all cities.
3. Calculate the average annual temperature for a specific city and year.
4. Calculate the average seven-day precipitation for a specific city and start date.
5. Calculate the average mean temperature by city within a date range.
6. Calculate the average annual precipitation by country for a specific year.
7. x. Quit the application.
## Notes
- Make sure to handle any required database configurations before running the script.
- The script uses the Colorama library for console text formatting. Ensure it is installed as part of the requirements.


# Phase 2 Readme file
## WeatherPlotter Application

### Installation Instructions

1. Ensure you have Python installed on your machine. If not, download and install it from python.org.

2. Navigate to the project directory.


   ```bash
   cd <project_directory>


3. Install the required dependencies.


   ```bash
   pip install matplotlib pandas colorama



4. Run the phase_2 class WeatherPlotter application.


   ```bash
   python phase_2.py

- Replace <filename> with the actual name of the Python script containing the WeatherPlotter class.

## Database Setup
The script uses an SQLite database located at db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db.

## Usage
1. Run the application using the provided installation instructions.
2. Follow the on-screen menu to choose an option (1-7) or 'x' to quit.
3. Enter the required information as prompted by the selected option.

## Chart Details
1. Plots seven-day precipitation data.
- Enter the start date (YYYY-MM-DD) to view a bar chart of precipitation for the next seven days.
2. Plots seven-day precipitation data for a specific city.
- Enter the start date (YYYY-MM-DD) and the name of the city to view a bar chart of precipitation for that city over the next seven days.
3. Plots precipitation data for multiple cities within a date range.
- Enter the start date (YYYY-MM-DD), end date (YYYY-MM-DD), and a comma-separated list of cities to view a bar chart of precipitation for the specified cities within the given date range.
4. Plots average yearly precipitation data by country.
- View a bar chart showing the average yearly precipitation for each country.
5. Bar charts for selected locations.
- Enter a comma-separated list of locations (cities, countries, etc.) to view a grouped bar chart showing the min/max/mean temperature and precipitation values for each location.
6. Plots daily temperature data for a specific city and month.
- Enter the city, year (YYYY), and month (MM) to view a multi-line chart of daily min/max temperatures for the specified city during the given month.
7. Plots scatter plot comparing average temperature and rainfall for multiple locations.
- Enter a location (city, country, etc.) to view a scatter plot comparing average temperature against average rainfall for the specified location.


- X. Quit
Exits the Weather Plotter.

### Notes
- Make sure to provide valid input when prompted.
- Handle interruptions (Ctrl+C) gracefully.
- Ensure the database file ("CIS4044-N-SDI-OPENMETEO-PARTIAL.db") is present in the "db" directory.
#### Feel free to explore and visualize weather data using the Weather Plotter!


# Phase 3 Readme
This phase implement deleting weather data from the sqlite data base and also provide menu system for the historical weather application.

## Installation
Before running the script, make sure you have Python installed on your system. You can download Python from the official Python website.


1. Install the required dependencies.

    ```bash
        pip install -r requirements.txt

2. Run the script.

    ```bash
    python phase_3.py

## Usage
The script provides a menu-driven interface with different phases. Follow the on-screen instructions to navigate through the phases and perform various operations.

1. Phases
- Phase 1: View Weather Data
- View weather data for a specific city and country.

2. Phase 2: Plot Weather Data
- Plot weather data for a specific city and country.

3. Phase 3: Delete Weather Data
- Delete weather entries based on city, country, and date range.

4. Phase 4: Add or Update Weather Data
- Add new weather data or update existing entries.

5. Exit
- Exit the weather application.


### Note
- Ensure that the SQLite database file (CIS4044-N-SDI-OPENMETEO-PARTIAL.db) is present in the db directory.

## Additional Information
- The script uses the WeatherApp, WeatherPlotter, AddOrUpdateWeatherAppData, and DeleteWeatherAppData classes from phase_1, phase_2, phase_4, and the current script.

- The styling for messages is handled by the WeatherApp class.
Support


# Phase 4 Inserting and Updating Weather Data

## Introduction
This Python script is designed to process weather data using the Open-Meteo API and store the information in a SQLite database. The application uses the geopy library to get latitude and longitude based on user input and the timezonefinder library to retrieve the timezone of the location. The processed weather data is then stored in the SQLite database, including information such as daily temperature, precipitation, and location details.

# Installation
Before running the script, ensure that you have the required Python libraries installed. You can install them using the following command:

    bash
    ```
    pip install timezonefinder geopy requests

## Database Setup
The script uses an SQLite database located at db/CIS4044-N-SDI-OPENMETEO-PARTIAL.db

# Running the Script
1. Open a terminal or command prompt.
2. Navigate to the directory containing the script.
3. Run the script using the following command:
    ```bash
    python phase_4.py

or Replace phase_4.py with the actual name of your Python script.

## Usage
- The script will prompt you to enter the city name for which you want to fetch and store weather data.
- Provide the start date and end date in the format YYYY-MM-DD.
The script will process the weather data for the specified city and store it in the database.
- If the country or city already exists in the database, the script will update the existing records; otherwise, it will create new entries.

## Note
- Ensure that your script contains the required libraries and is structured correctly before running it.

