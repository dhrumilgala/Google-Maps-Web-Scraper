GOOGLE MAPS BUSINESS SCRAPER


OVERVIEW:

This Python script automates the process of searching for businesses on Google Maps, extracting key details such as the business name, address, website, phone number, and geographic coordinates, and saving the data into structured files (Excel and CSV). The script is designed to be flexible and can handle multiple search terms provided via command-line arguments or a text file.


FEATURES:

Automated Data Extraction: Extracts business details like name, address, website, phone number, and coordinates directly from Google Maps.
Flexible Search Options: Accepts search terms via command-line arguments or an input text file.
Multiple Output Formats: Saves results as Excel and CSV files.
Error Handling: Includes basic error handling to manage issues during the scraping process.
Headless Mode: Supports running the browser in headless mode for faster execution and reduced resource usage.
Save Location: Customize the output directory where files are saved.


REQUIREMENTS:

Python 3.7+
Google Chrome browser
ChromeDriver (managed automatically by webdriver_manager)
Required Python packages:
selenium
pandas
webdriver_manager


INSTALLATION AND SETUP:

cd google_web_scraper

pip install -r requirements.txt

Note: The script uses webdriver_manager to automatically handle ChromeDriver installation. Ensure that you have the Chrome browser installed.


USAGE:

python main.py -s "Coffee Shops in San Francisco" -t 5

WHERE
-s or --search: The search term you want to use on Google Maps.
-t or --total: The number of results to scrape. Defaults to 5 if not specified.


Alternatively, you can provide search terms in a text file named input.txt, with one search term per line:

python main.py


OUTPUT:

The script will save the extracted data into Excel and CSV files in the output directory. The filenames are based on the search term, with spaces replaced by underscores. For example:

google_maps_data_Coffee_Shops_in_San_Francisco.xlsx
google_maps_data_Coffee_Shops_in_San_Francisco.csv


HEADLESS MODE:

If you want to run the script in headless mode (i.e., without opening a visible browser window), you can enable this by modifying the headless option in the script:

options.headless = True


