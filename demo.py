import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Read credentials from Excel file
file_path = 'Credentials.xlsx'
credentials = pd.read_excel(file_path, skiprows=3, usecols=[1, 2], names=['User ID', 'Password'])

chrome_driver_path = r"C:\Users\Lalith\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Specify download directory path
download_dir = r'C:\Users\Lalith\Downloads'

# Configure Chrome options for file download
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    'download.default_directory': download_dir,
    'download.prompt_for_download': False,
    'download.directory_upgrade': True,
    'safebrowsing.enabled': True
})

# Initialize Chrome WebDriver with options and path
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=chrome_options)

# Iterate over the credentials
for index, row in credentials.iterrows():
    user_id = row['User ID']
    password = row['Password']

    try:
        # Navigate to the desired URL
        driver.get("https://login.wowway.com/Default.aspx")

        # Wait for the username input element to be present
        wait = WebDriverWait(driver, 10)
        username_input = wait.until(
            EC.presence_of_element_located((By.NAME, "username")))

        # Enter the username
        username_input.send_keys(user_id)

        # Locate the password input element and enter the password
        password_input = driver.find_element(By.NAME, "password")
        password_input.send_keys(password)

        # Locate and click the login button
        login_button = driver.find_element(By.ID, "submit-button")
        login_button.click()

        time.sleep(20)

        # Locate the target button and click it
        target_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#__next > div > div.page-container > div.content-wrapper > div > div:nth-child(2) > div > div:nth-child(2) > div > div > div:nth-child(1) > div > div > div > div:nth-child(2) > div > div > div:nth-child(2) > div > div:nth-child(1) > span > a > div > p")))

        # Scroll to the button to ensure it is in view
        driver.execute_script("arguments[0].scrollIntoView();", target_button)

        # Click the target button
        target_button.click()
        time.sleep(15)

        # Locate the download button and click it
        button = wait.until(EC.presence_of_element_located(
            (By.XPATH,
            "//button[contains(@class, 'MuiButtonBase-root') and .//span[text()='download']]")
        ))

        # Scroll to the element to ensure it is in view
        driver.execute_script("arguments[0].scrollIntoView();", button)

        # Click the button
        button.click()
        time.sleep(10)
    finally:
        # Close the WebDriver
        driver.quit()
