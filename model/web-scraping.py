#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# get_ipython().run_line_magic('pip', 'install sel





# In[ ]:


from selenium import webdriver
import argparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
url=input("Enter the URL")
driver = webdriver.Chrome()
driver.get(url)
url = driver.current_url
# print(url)
parts = url.split("/")
element_name = parts[-1]
# print(element_name)


# In[ ]:


from selenium import webdriver
import re
import csv

def find_elements_by_regex_href(driver, regex_pattern):
    elements = driver.find_elements_by_tag_name("a")
    filtered_elements = [element for element in elements if re.search(regex_pattern, element.get_attribute("href"))]
    return filtered_elements

# def open_link():
#      elemental = driver.find_element_by_class_name("d-flex align-items-center")
#      href = elemental.get_attribute("href")
#      print("Extracted href:", href)
#      elemental.click()


# Define the regex pattern for href attribute
regex_pattern = rf"https://fueler.io/{element_name}/."
# Find elements matching the regex pattern
# skills=find_elements("mb-0 px-3 py-2 text-dark-blue")
elements = find_elements_by_regex_href(driver, regex_pattern)

# Iterate through the matching elements
for i, element in enumerate(elements):
    if i < 2:
        continue  # Skip the first two elements
    else:
            link_href = element.get_attribute("href")
            driver.execute_script("window.open(arguments[0], '_blank');", link_href)
            driver.switch_to.window(driver.window_handles[-1])
            new_tab_url = driver.current_url
            elements = driver.find_elements_by_class_name("work-key-word-btn")
            print(text_contents)
            text_contents = [element.text for element in elements]
            csv_file = "text_contents.csv"
            with open(csv_file, mode='a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([text_contents])

            # for text in text_contents:
            #     print("Extracted text:", text)
            

            # print("Current URL of the new tab:", new_tab_url)
            # driver.close()
            # open_link()
            # driver.execute_script("window.open(arguments[0], '_blank');", link_href)
            # driver.switch_to.window(driver.window_handles[-1])
            # new_tab_url = driver.current_url
            # open_link()
            # driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.window(driver.window_handles[0])
        # except Exception as e:
        #     print(f"Error clicking or extracting href: {e}")

driver.quit()

