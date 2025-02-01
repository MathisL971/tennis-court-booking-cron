from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# Initialize WebDriver
service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Open the login page
    driver.get("https://book.stadeiga.com/courtbooking/home/reportView.do?id=74&history=clear")

    # Wait for the page to load and locate input fields
    wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds for elements to appear

    # Find and input username and password
    userid_field = wait.until(EC.presence_of_element_located((By.ID, "userid")))
    password_field = driver.find_element(By.ID, "password")

    userid_field.send_keys("lefrancmathis@gmail.com")
    password_field.send_keys("BrebeufMTL5174$")

    # Press ENTER to submit the form
    password_field.send_keys(Keys.RETURN)

    # Wait for the page to load after login
    time.sleep(3)

    # Click the anchor tag with the exact text "Book Indoor Hard Courts (12 Courts)"
    court_booking_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Book Indoor Hard Courts (12 Courts)']"))
    )
    court_booking_link.click()

    print("Successfully clicked the court booking link!")

    time.sleep(3)  # Wait to observe the result

    # Find the div with id "caldaylink"
    caldaylink_div = wait.until(EC.presence_of_element_located((By.ID, "caldaylink")))

    # Iterate over all child anchor tags and click each
    anchor_tags = caldaylink_div.find_elements(By.TAG_NAME, "a")

    print(f"Available links in 'caldaylink' div: {len(anchor_tags)}")

    for index, anchor in enumerate(anchor_tags):
        try:
            print(f"Clicking link {index + 1}: {anchor.text}")
            driver.execute_script("arguments[0].click();", anchor)  # Click using JavaScript to avoid stale element issues
            time.sleep(3)  # Wait between each click to allow page updates
        except Exception as e:
            print(f"Error clicking link {index + 1}: {e}")

    print("Successfully clicked all available links in 'caldaylink' div!")

    time.sleep(5)  # Observe results

finally:
    driver.quit()  # Close the browser
