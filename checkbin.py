from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_bin_collection_info():
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()
    
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
    
    # Print the bin collection info
    print("Bin collection information:\n", bin_info)
    
    # Leave the browser open for a few seconds before closing
    time.sleep(10)  # Wait for 10 seconds before closing the browser

    # Clean up, close the browser
    driver.quit()
    
    # Return the bin info for any further processing
    return bin_info

# Example usage
get_bin_collection_info()