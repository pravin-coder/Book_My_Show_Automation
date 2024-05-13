from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import tkinter as tk
from tkinter import simpledialog
import pandas as pd
from pandas.api.types import CategoricalDtype
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import traceback
import time
import random
import winsound


def establish_connection():
    try:
        # Set the path to GeckoDriver executable
        geckodriver_path = "C:/Program Files/geckodriver.exe"  # Update with the actual path
        
        # Set the path to your Firefox binary
        firefox_binary_path = "C:/Program Files/Mozilla Firefox/firefox.exe"  # Use forward slashes or double backslashes
        
        # Set Firefox binary option
        firefox_options = Options()
        firefox_options.binary_location = firefox_binary_path
        
        driver = webdriver.Firefox(options=firefox_options, executable_path=geckodriver_path)
        return driver
    except Exception as e:
        print("An error occurred while establishing connection:", str(e))
        traceback.print_exc()  # Print full traceback   
        return None

def login(driver, mobile_number):
    try:
        driver.get("https://in.bookmyshow.com/explore/home/chennai")
        
        # Wait for the obscuring element to disappear
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".bwc__sc-1ihur1g-4.jxHGrI.in-animation"))
        )
        
        # Scroll to the button
        button = driver.find_element(By.CSS_SELECTOR, ".bwc__sc-1nbn7v6-14.khhVFa")
        driver.execute_script("arguments[0].scrollIntoView();", button)
        
        # Click the button using JavaScript
        driver.execute_script("arguments[0].click();", button)
        
        mobile_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "mobileNo"))
        )
        # Enter mobile number
        mobile_input.send_keys(mobile_number)
        # Simulate pressing the enter key
        mobile_input.send_keys(Keys.ENTER)
        
        # Wait for the PIN input fields to be clickable
        pin_inputs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.bwc__sc-m1rlyj-3 input"))
        )
        
        # Enter PIN code into input fields
        pin_code = input("Enter the pin code which was sent to your mobile number: ")
        for i, digit in enumerate(pin_code):
            pin_inputs[i].send_keys(digit)
        
        # Press Enter key after entering all digits
        pin_inputs[-1].send_keys(Keys.ENTER)
        time.sleep(10)
    except Exception as e:
        print("An error occurred while logging in:", str(e))
        traceback.print_exc()  # Print full traceback   
        driver.quit()
        
def theater(driver,T_name):
    try:
        search_bar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='4' and @class='bwc__sc-1nbn7v6-8 hbuyht']"))
        )
        search_bar.click()
        
        # Wait for the search input field to be clickable and focused
        theater_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.bwc__sc-1iyhybo-6.ilhhay"))
        )
        
        # Clear the input field before sending the keys
        theater_input.clear()
        # Enter movie theater name
        theater_input.send_keys(T_name)
        
        # Submit the form (press Enter)
        theater = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.bwc__sc-3t17w7-58.fjWgDR"))
        )
        theater.click()
    except Exception as e:
        print("An error occurred while searching for movie:", str(e))
        traceback.print_exc()  # Print full traceback   
        driver.quit()

def  movie_search(driver, movie_to_search, no_of_seat,row,seat_no):
    try:
        attempt = 1
        while True:
            movie_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'nameSpan')]")

            for movie_element in movie_elements:
                movie_name = movie_element.text.strip()
                if movie_to_search in movie_name:
                    print(f"Movie found: {movie_name}")

                    # Find the parent container of the movie element
                    parent_container = movie_element.find_element(By.XPATH, "./ancestor::li[contains(@class, 'list')]")

                    # Find the showtime pill container for the corresponding movie
                    showtime_container = WebDriverWait(parent_container, 10).until(
                        EC.presence_of_element_located((By.XPATH, ".//a[contains(@class, 'showtime-pill') and contains(@class, 'data-enabled')]"))
                    )

                    # Dismiss overlay if it exists

                    # Extract screen name
                    screen_name = showtime_container.find_element(By.CLASS_NAME, 'attribute').text.strip()

                    # Scroll the showtime container into view
                    driver.execute_script("arguments[0].scrollIntoView(true);", showtime_container)

                    # Wait for a brief moment
                    time.sleep(1)
                    dismiss_overlay(driver)
                    # Click on the showtime pill of the corresponding movie using JavaScript
                    driver.execute_script("arguments[0].click();", showtime_container)
                    dismiss_overlay(driver)
                    
                    print(f"Booking seats in {screen_name}.")
                    select_seat(driver,no_of_seat,row,seat_no)
                    return  # Exit the function after finding the movie

            # If movie is not found, wait for a random time between 1 and 100 seconds and refresh the page
            wait_time = random.randint(1, 100)
            print(f"Movie '{movie_to_search}' not found. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)  # Wait for a random time between 1 and 100 seconds
            driver.refresh()  # Refresh the page

        else:
            print(f"Movie '{movie_to_search}' not found after {max_retries} retries.")
    
    except Exception as e:
        print("An error occurred:", e)
        traceback.print_exc()  # Print the traceback for debugging

def dismiss_overlay(driver):
    try:
        # Find and dismiss overlay if it exists
        overlay = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.ID, "wzrk-cancel"))  # Update class name accordingly
        )
        overlay.click()
    except:
        pass

def select_seat(driver,no_of_seat,row,seat_no):
    try:
        # Dismiss overlay if it exists
        dismiss_overlay(driver)
        # Wait for the seat element corresponding to the desired number of seats to be clickable
        seat_id = f"pop_{no_of_seat}"
        seat_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, seat_id))
        )
        dismiss_overlay(driver)
        seat_button.click()
        
        # Find and click the "Select Seats" button
        select_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "proceed-Qty"))
        )
        dismiss_overlay(driver)
        select_button.click() 
        #running this while loop untill the ticket is available 
        table = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "setmain"))
        )
        condition=True   
        #running this while loop untill the ticket is available 
        while condition:
            tr_tags = table.find_elements(By.TAG_NAME, "tr")
            r=int(len(tr_tags))
            flg=0
            for index, tr_tag in enumerate(tr_tags):
                td_tag = tr_tag.find_element(By.TAG_NAME, "td")
                row_index = td_tag.text.strip()
                if row in row_index:
                    n=index+1
        
            # Find the nth <tr> element
            xpath = f"//tbody/tr[{n}]"
            tr_element = table.find_element(By.XPATH, xpath)
            xpath_td = f"./td[2]"  # Updated XPath to select the second <td> element
            td_element = tr_element.find_element(By.XPATH, xpath_td)
            # Find all <div> tags inside the <td> element
            div_elements = td_element.find_elements(By.XPATH, "./div")
            l=len(div_elements)
            flg=0   
            # Iterate over each <div> element and check if '6' is in the <a> tag text
            for index, div_element in enumerate(div_elements):
                try:
                    a_element = div_element.find_element(By.TAG_NAME, "a")
                    x=str(seat_no)
                    if x in a_element.text.strip():
                        if(a_element.get_attribute("class")=="_available"):
                            try:
                                driver.execute_script("arguments[0].scrollIntoView(false);", div_element)
                                div_element.click()
                                
                            except Exception as e:
                                # Scroll the parent container into view
                                driver.execute_script("arguments[0].scrollIntoView(true);", div_element)
                                # Now you can click on the <div> element
                                div_element.click()
                            print(f"seats Booked on {row} - row ,seat-no - {Seat_no}")
                            condition=False
                            break  # Exit loop once the desired div element is found
                        
                        elif(a_element.get_attribute("class")=="_blocked"):
                            flg=1
                            break
                        
                except NoSuchElementException:
                    continue 
            if(flg==1):
                print("sorry! the seat you are willing to book is already been booked by someone,so searching for next seats ") 
                terminate = False
                for i in range(4,len(div_elements)-4):
                    index=0
                    for index in range(len(div_elements)):
                        div_element = div_elements[index]              
                        try:
                            a_element = div_element.find_element(By.TAG_NAME, "a")
                            if str(i) in a_element.text.strip():
                                if(a_element.get_attribute("class")=="_available"):
                                    try:
                                        driver.execute_script("arguments[0].scrollIntoView(false);", div_element)
                                        div_element.click()
                                
                                    except Exception as e:
                                        # Scroll the parent container into view
                                        driver.execute_script("arguments[0].scrollIntoView(true);", div_element)
                                        # Now you can click on the <div> element
                                        div_element.click()
                                    print(f"Booked seat on {row} - row ,seat-no - {i}")
                                    condition=False
                                    terminate = True
                                    break  # Exit loop once the desired div element is found
                                
                                elif(a_element.get_attribute("class")=="_blocked"):
                                    break
                    
                        except NoSuchElementException:
                            continue
                 
                    if terminate:    
                        # if the seat is found then no need for search the next seat                
                        break
            
                if terminate==False:    
                    # if the seat is found then no need for search the next seat                
                    print("sorry ,No seats are found in this row")    

            if(condition==True):
                print(f"Since there is no seats in row {row},so booking the same seat in next row")            
                asci = ord(row)
                row=chr(asci+1)
        else:
            print("seat booked successfully ")

    except Exception as e:
        print("An error occurred during seat selection:", e)
        
def payment(driver,mobile_number,e_mail):
    try:
        # Find the accept button by ID
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btmcntbook"))
        )
        
        # Click the accept button
        accept_button.click()
        accept_button2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btnPopupAccept"))
        )
        # Click the accept button
        accept_button2.click()   
        
        proceed_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "prePay"))
        )
        
        # Click the second "Proceed" button
        proceed_button.click()
        
        # Wait for email input field to be visible and interactable
        email_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "txtEmail"))
        )
        
        # Scroll to the email input field
        driver.execute_script("arguments[0].scrollIntoView(true);", email_input)
        
        # Input email address
        email_input.send_keys(e_mail)
        
        mobile_number = "+91" + mobile_number
        # Locate and input mobile number
        mobile_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "txtMobile"))
        )
        mobile_input.clear() 
        mobile_input.send_keys(mobile_number)  
        
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@data-auto='contact-details-continue']"))
        )
        # Click the continue button
        continue_button.click()
        
    except Exception as e:
        print("An error occurred:", e)
        
def beep_sound():
    duration = 1000  # milliseconds
    frequency = 440  # Hz
    end_time = time.time() + 20  # 20 seconds from current time

    while time.time() < end_time:
        winsound.Beep(frequency, duration)
        time.sleep(1)
        
def main():
    try:
        root = tk.Tk()
        root.withdraw() 
        print("\t\t\t\t===============================================")
        print("\t\t\t\t||               WELCOME                    ||")
        print("\t\t\t\t===============================================")
        print("NOTE: pleasemake sure that you have installed firefox browser") 
        
        mobile_number = input("please enter your mobile number: ")
        e_mail=input("please enter your E-mail id: ")
        T_name=input("Enter the name of the theater: ")
        movie_to_search =input("Please enter the movie name: ") 
        print("you can only book one seat")
        no_of_seat = 1
        row=input("Enter the row name: ")
        row=row[0].upper()
        seat_no=int(input("Enter the seat number you want to book: "))
        driver = establish_connection()
        if driver:
            login(driver, mobile_number)
            theater(driver,T_name)
            movie_search(driver, movie_to_search, no_of_seat,row,seat_no)
            payment(driver,mobile_number,e_mail)
            print("Ticket Booked successfully,make payment and you will get your ticket through mail / whatsapp")
            beep_sound()
    except Exception as e:
        print("An error occurred in the main function:", str(e))
        traceback.print_exc()  # Print full traceback   
        driver.quit()

if __name__ == "__main__":
    main()
        