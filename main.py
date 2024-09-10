from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys
from webdriver_manager.chrome import ChromeDriverManager
import time

@dataclass
class Business:
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None
    latitude: float = None
    longitude: float = None

@dataclass
class BusinessList:
    business_list: list[Business] = field(default_factory=list)
    save_at = 'output'

    def dataframe(self):
        return pd.json_normalize(
            (asdict(business) for business in self.business_list), sep="_"
        )

    def save_to_excel(self, filename):
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_excel(f"{self.save_at}/{filename}.xlsx", index=False)

    def save_to_csv(self, filename):
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"{self.save_at}/{filename}.csv", index=False)

def extract_coordinates_from_url(url: str) -> tuple[float, float]:
    coordinates = url.split('/@')[-1].split('/')[0]
    return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()

    search_list = [args.search] if args.search else []
    total = args.total if args.total else 5  # Ensure we only want top 5 results

    if not args.search:
        input_file_name = 'input.txt'
        input_file_path = os.path.join(os.getcwd(), input_file_name)
        if os.path.exists(input_file_path):
            with open(input_file_path, 'r') as file:
                search_list = file.readlines()
        if len(search_list) == 0:
            print('Error occurred: You must either pass the -s search argument, or add searches to input.txt')
            sys.exit()

    options = Options()
    options.headless = False
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for search_for_index, search_for in enumerate(search_list):
        search_for = search_for.strip()  # Remove any extra whitespace
        print(f"-----\n{search_for_index} - {search_for}")

        driver.get("https://www.google.com/maps")
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys(search_for)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)  # wait for the results to load

        business_list = BusinessList()

        # Get the top 5 results' URLs
        top_results_urls = []
        while len(top_results_urls) < total:
            listings = driver.find_elements(By.XPATH, '//a[contains(@href, "/place/") and not(contains(@aria-label, "Sponsored"))]')
            for listing in listings:
                if len(top_results_urls) >= total:
                    break
                url = listing.get_attribute("href")
                if url not in top_results_urls:
                    top_results_urls.append(url)

            if len(top_results_urls) < total:
                driver.execute_script("window.scrollBy(0, 1000);")
                time.sleep(2)  # give time for more listings to load

        # Extract details from each top result using the URLs
        for index, url in enumerate(top_results_urls):
            try:
                driver.get(url)
                time.sleep(3)  # wait for the details to load

                try:
                    name = driver.find_element(By.XPATH, '//h1[contains(@class, "DUwDvf lfPIob")]').text
                except Exception:
                    name = driver.find_element(By.XPATH, '//h1[contains(@class, "fontHeadlineLarge")]').text
                business = Business(name=name)

                # Extract details
                try:
                    business.address = driver.find_element(By.XPATH, '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]').text
                except Exception:
                    business.address = None

                try:
                    business.website = driver.find_element(By.XPATH, '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]').text
                except Exception:
                    business.website = None

                try:
                    business.phone_number = driver.find_element(By.XPATH, '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]').text
                except Exception:
                    business.phone_number = None

                try:
                    business.latitude, business.longitude = extract_coordinates_from_url(driver.current_url)
                except Exception:
                    business.latitude, business.longitude = None, None

                business_list.business_list.append(business)
                print(f"Scraped {index + 1}/{len(top_results_urls)}: {business.name}")

            except Exception as e:
                print(f'Error occurred: {e}')

        business_list.save_to_excel(f"google_maps_data_{search_for}".replace(' ', '_'))
        business_list.save_to_csv(f"google_maps_data_{search_for}".replace(' ', '_'))

    driver.quit()

if __name__ == "__main__":
    main()
