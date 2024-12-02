from math import isnan

import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.service import Service

def open_places_and_save_with_selenium(data):
    service = Service(executable_path='./chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--user-data-dir=C:\\Users\\kylek\\AppData\\Local\\Google\\Chrome\\User Data")  # Replace with your actual path
    driver = webdriver.Chrome(service=service, options=options)

    try:
        start_from = 837
        index = -1
        for _, row in data.iterrows():
            index += 1
            if index < start_from:
                continue
            url = row['URL']
            if pd.notnull(url):
                print(f"Opening: {row['Title']} - {url}")
                driver.get(url)
                time.sleep(2)

                try:
                    driver.find_element(By.XPATH, "//span[contains(@class, 'Cw1rxd google-symbols NhBTye Cdyak')]")
                    already_saved = True
                except NoSuchElementException:
                    already_saved = False
                if already_saved:
                    print("Already saved.")
                else:
                    save_button = driver.find_elements(By.XPATH, "//span[contains(@class, 'PHazN')]")[0]
                    save_button.click()
                    time.sleep(2)

                    try:
                        list_to_add = driver.find_elements(By.XPATH, "//*[contains(@class, 'MMWRwe fxNQSd')]")[1]
                    except IndexError:
                        # probably doesn't exist anymore
                        print("Place doesn't exist.")
                        continue
                    list_to_add.click()
                    time.sleep(2)

                if isinstance(row["Note"], str):
                    try:
                        driver.find_element(By.XPATH, "//*[contains(@class, 'HlvSq OazX1c')]")
                        already_has_note = True
                    except NoSuchElementException:
                        already_has_note = False

                    if already_has_note:
                        print("Already has note.")
                    else:
                        note_dropdown_arrow = driver.find_elements(By.XPATH, "//*[contains(@class, 'Cw1rxd google-symbols SwaGS')]")[0]
                        note_dropdown_arrow.click()
                        time.sleep(2)
                        add_note_button = driver.find_element(By.XPATH, '//*[@aria-label="Add note in Want to go"]')
                        add_note_button.click()
                        time.sleep(2)
                        text_area = driver.find_element(By.XPATH, "//*[contains(@class, 'sbPorb gRsCne azQIhc')]")
                        text_area.send_keys(row["Note"])
                        time.sleep(1)
                        done_button = driver.find_element(By.XPATH, "//*[contains(@class, 'okDpye PpaGLb mta2Ab')]")
                        done_button.click()
                        time.sleep(2)
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = "./Want to go.csv"
    csv_data = pd.read_csv(file_path)

    data_to_process = csv_data[['Title', 'Note', 'URL']]

    open_places_and_save_with_selenium(data_to_process)
