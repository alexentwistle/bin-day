from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_bin_collection_info():
    # Set up the Selenium WebDriver
    driver = webdriver.Chrome()
    
    # Navigate to the bin collection page
    driver.get("https://www.enfield.gov.uk/services/rubbish-and-recycling/find-my-collection-day")
    
    # Wait for the page to load completely
    time.sleep(2)
    
    # Take user input for postcode and address
    user_input = input("Please enter your postcode and address: ")
    
    # Locate the search input field by ID and enter the user input
    search_input = driver.find_element(By.ID, 'myText0')
    search_input.send_keys(user_input)
    time.sleep(2)  # Wait for the dropdown to populate. TODO: may need to click 'search'
    
    # Press the down arrow to select the top result from the dropdown
    search_input.send_keys(Keys.ARROW_DOWN)
    time.sleep(1)  # Ensure selection is highlighted
    
    # Press Enter to confirm the selection
    search_input.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for any page updates
    
    # Optionally, navigate and extract specific information about bin collection
    # For example, locating the element that contains the bin collection details. UPDATE.
    bin_info = driver.find_element(By.CLASS_NAME, 'bin-collection-details').text

    # Clean up, close the browser
    driver.quit()
    
    # Return or print any relevant information. UPDATE.
    return bin_info

# Example usage
get_bin_collection_info()
