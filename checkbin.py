from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
from datetime import datetime

def parse_date(bin_description):
    # Extracts the date from the string using regex and converts it to a datetime object
    date_match = re.search(r'\d{2}/\d{2}/\d{4}', bin_description)
    if date_match:
        return datetime.strptime(date_match.group(), '%d/%m/%Y')
    return None

def get_next_bin_collection(bin_info):
    # Split the bin_info into separate lines
    lines = bin_info.split('\n')
    # Initialize a dictionary to hold the date for each type of bin
    bin_dates = {}
    for line in lines:
        if 'black bin collection date is' in line:
            date = parse_date(line)
            if date:
                bin_dates['black'] = date
        elif 'blue bin collection date is' in line:
            date = parse_date(line)
            if date:
                bin_dates['blue'] = date
    
    # Determine which bin has the earlier collection date
    if bin_dates:
        next_bin = min(bin_dates, key=bin_dates.get)
        return f"The next bin to be collected is the {next_bin} bin on {bin_dates[next_bin].strftime('%d/%m/%Y')}."
    return "No bin collection dates found."

def get_bin_collection_info():
    # Set up Chrome options for headless mode
    options = Options()
    options.headless = True
    options.add_argument('--log-level=3')  # This should suppress most of the console logs
    
    # Set up the Selenium WebDriver with the specified options
    driver = webdriver.Chrome(options=options)
    
    # Navigate to the bin collection page
    driver.get("https://www.enfield.gov.uk/services/rubbish-and-recycling/find-my-collection-day")
    
    # Wait for the page to load completely
    time.sleep(2)
    
    # Dismiss cookie consent popup
    try:
        cookie_button = driver.find_element(By.ID, 'ccc-notify-reject')
        cookie_button.click()
    except Exception as e:
        print("Cookie consent popup was not found or could not be dismissed:", str(e))
    WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.ID, 'ccc-notify-reject')))
    
    # Take user input for postcode and address
    user_input = input("Please enter your postcode and address: ")
    
    # Locate the search input field by ID and enter the user input
    search_input = driver.find_element(By.ID, 'myText0')
    search_input.send_keys(user_input)
    
    # Click the search button
    search_button = driver.find_element(By.ID, 'submitButton0')
    search_button.click()
    
    # Handle dropdown menu
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'mySelect0')))
    dropdown = driver.find_element(By.ID, 'mySelect0')
    dropdown.click()  # Explicitly click to open the dropdown

    # Explicitly select the first option with class 'select-option'
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.select-option')))
    first_option = driver.find_elements(By.CSS_SELECTOR, '.select-option')[0]
    first_option.click()  # Click the first select-option
    time.sleep(2)  # Wait for any AJAX calls or updates to be completed
    
    # Wait for the bin collection details to be visible
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'results')))
    bin_info = driver.find_element(By.ID, 'results').text
    
    # Print the bin collection info. Uncomment if needed.
    # print("Bin collection information:\n", bin_info)
    
    # Determine and print which bin is next to be collected
    next_bin_collection = get_next_bin_collection(bin_info)
    print(next_bin_collection)
    
    # Clean up, close the browser
    driver.quit()
    
    # Return the bin info for any further processing
    return bin_info

# Example usage
get_bin_collection_info()
