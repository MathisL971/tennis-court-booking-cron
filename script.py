# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# # Set Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--start-maximized")
# service = Service(ChromeDriverManager().install())

# driver = webdriver.Chrome(service=service, options=chrome_options)

# DAY_PRIVILEGE = 3

# try:
#     # Open the login page
#     driver.get("https://book.stadeiga.com/courtbooking/home/reportView.do?id=74")

#     # Wait for the page to load and locate input fields
#     wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds for elements to appear

#     # Find and input username and password
#     userid_field = wait.until(EC.visibility_of_element_located((By.ID, "userid")))
#     password_field = driver.find_element(By.ID, "password")

#     userid_field.send_keys("lefrancmathis@gmail.com")
#     password_field.send_keys("BrebeufMTL5174$")
#     # userid_field.send_keys("gautier.diebolt@hotmail.com")
#     # password_field.send_keys("TennisIGA")

#     # Press ENTER to submit the form
#     password_field.send_keys(Keys.RETURN)

#     # Wait for the page to load after login
#     time.sleep(3)

#     # Click the anchor tag with the exact text "Book Indoor Hard Courts (12 Courts)"
#     court_booking_link = wait.until(
#         EC.element_to_be_clickable((By.XPATH, "//a[text()='Book Indoor Hard Courts (12 Courts)']"))
#     )
#     court_booking_link.click()

#     print("Successfully clicked the court booking link!")

#     time.sleep(3)  # Wait to observe the result

#     courts_available_details = []

#     for index in range(DAY_PRIVILEGE):
#         try:
#             # Find the div with id "caldaylink"
#             caldaylink_div = wait.until(EC.presence_of_element_located((By.ID, "caldaylink")))

#             # Iterate over all child anchor tags and click each
#             anchor_tags = caldaylink_div.find_elements(By.TAG_NAME, "a")

#             anchor = anchor_tags[index]
#             date = anchor.text[2:-2]

#             print(f"Clicking link {index + 1}: {anchor.text}")

#             # driver.execute_script("arguments[0].click();", anchor)
#             anchor.click()

#             time.sleep(3)

#             # Find table tag with classname "calendar"
#             table_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "calendar")))

#             # Get the tbody element from the table tag
#             tbody = table_tag.find_element(By.TAG_NAME, "tbody")

#             #Iterate over all rows in the tbody starting from the second row
#             for row in tbody.find_elements(By.TAG_NAME, "tr")[1:]:
#                 court = row.find_elements(By.TAG_NAME, "td")[0].text
#                 # Iterate over all cells in the row
#                 for cell in row.find_elements(By.TAG_NAME, "td")[1:]:
#                     # If bgcolor is #FFFFFF, click the cell
#                     if cell.get_attribute("bgcolor") == "#FFFFFF":
#                         # If index 0 and time is past the current time, click the cell
#                         if index == 0 and cell.text.split()[1] < time.strftime("%H:%M"):
#                             # Continue
#                             continue

#                         # Print court and time (which is the text of the cell)
#                         print(f"Court: {court}, Date: {date}, Time: {cell.text.split()[1]}")

#                         courts_available_details.append(
#                             {
#                                 "court": court,
#                                 "date": date,
#                                 "time": cell.text.split()[1],
#                             }
#                         )

#                         # Click the cell
#                         cell.click()
#                         time.sleep(3)

#                         # Go back to the previous page
#                         driver.back()
#                         time.sleep(3)

#         except Exception as e:
#             print(f"Error clicking link {index + 1}: {e}")

#     print("Successfully clicked all available links in 'caldaylink' div!")

#     # Send email with courts_available_details
#     # TODO

#     time.sleep(5)  # Observe results

# finally:
#     driver.quit()  # Close the browser

import smtplib
import logging
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

load_dotenv()

# Configure logging
logging.basicConfig(
    filename="court_booking.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logging.info("Script started.")

# Email settings
SMTP_SERVER = "smtp.gmail.com"  # Change this if using another provider
SMTP_PORT = 587
EMAIL_SENDER = os.getenv("GMAIL_EMAIL")  # Replace with your email
EMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
EMAIL_RECEIVER = os.getenv("GMAIL_EMAIL")

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")  # Required for running in crontab
chrome_options.add_argument("--disable-gpu")  # Improve performance in headless mode
chrome_options.add_argument("--no-sandbox")  # Avoid permission issues in cron
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

DAY_PRIVILEGE = 3
courts_available_details = []

try:
    driver.get("https://book.stadeiga.com/courtbooking/home/reportView.do?id=74")
    wait = WebDriverWait(driver, 10)

    # Login
    userid_field = wait.until(EC.visibility_of_element_located((By.ID, "userid")))
    password_field = driver.find_element(By.ID, "password")

    userid_field.send_keys("lefrancmathis@gmail.com")
    password_field.send_keys("BrebeufMTL5174$")
    password_field.send_keys(Keys.RETURN)

    logging.info("Logged in successfully.")
    time.sleep(3)

    # Click "Book Indoor Hard Courts"
    court_booking_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Book Indoor Hard Courts (12 Courts)']"))
    )
    court_booking_link.click()
    logging.info("Navigated to court booking page.")

    time.sleep(3)

    for index in range(DAY_PRIVILEGE):
        try:
            caldaylink_div = wait.until(EC.presence_of_element_located((By.ID, "caldaylink")))
            anchor_tags = caldaylink_div.find_elements(By.TAG_NAME, "a")

            anchor = anchor_tags[index]
            date = anchor.text[2:-2]

            logging.info(f"Clicking link {index + 1}: {anchor.text}")
            anchor.click()

            time.sleep(3)

            table_tag = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "calendar")))
            tbody = table_tag.find_element(By.TAG_NAME, "tbody")

            for row in tbody.find_elements(By.TAG_NAME, "tr")[1:]:
                court = row.find_elements(By.TAG_NAME, "td")[0].text
                for cell in row.find_elements(By.TAG_NAME, "td")[1:]:
                    if cell.get_attribute("bgcolor") == "#FFFFFF":
                        if index == 0 and cell.text.split()[1] < time.strftime("%H:%M"):
                            continue

                        logging.info(f"Available: Court {court}, Date {date}, Time {cell.text.split()[1]}")
                        courts_available_details.append(f"Court: {court}, Date: {date}, Time: {cell.text.split()[1]}")

                        cell.click()
                        time.sleep(3)
                        driver.back()
                        time.sleep(3)

        except Exception as e:
            logging.error(f"Error clicking link {index + 1}: {e}")

    logging.info("Finished checking all court dates.")

    if courts_available_details:
        message = "Available courts:\n" + "\n".join(courts_available_details)
        logging.info("Sending email notification.")
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, f"Subject: Tennis Court Availability\n\n{message}")
    else:
        logging.info("No available courts found.")

finally:
    driver.quit()
    logging.info("Script finished.")
