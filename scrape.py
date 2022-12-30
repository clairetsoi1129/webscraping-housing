from bs4 import BeautifulSoup

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

# from csv import writer

import pandas as pd
import matplotlib.pyplot as plt

# Create driver
driver = webdriver.Chrome(ChromeDriverManager().install())

# Go to the apartments pages
page_url = "https://www.pararius.com/apartments/amsterdam"

driver.get(page_url)

# Wait util the agree button is loaded and click on it
el = WebDriverWait(driver, timeout=40).until(lambda d: d.find_element_by_id("onetrust-accept-btn-handler"))
assert el.text == "Agree"
el.click()

# Find the apartment info 
isHaveNextPage=True
page=1
apartment_list =[]
while (isHaveNextPage):
    driver.get(page_url+"/page-"+str(page))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    item_lists = soup.find_all("section", class_="listing-search-item")

    for item in item_lists:
        title = item.find("a", class_="listing-search-item__link--title").text.strip()
        location = item.find("div", class_="listing-search-item__sub-title").text.strip()
        price = item.find("div", class_="listing-search-item__price").text.strip()
        area = item.find("li", class_="illustrated-features__item--surface-area").text.strip()
        apartment_list.append({'title':title, 'location':location, 'price':price, 'area':area})

    page = page+1
    # Check if still have next page
    if soup.find("a",class_='pagination__link--next') is None:
        isHaveNextPage=False



# Write the info in csv file
apartment_df = pd.DataFrame(apartment_list)
apartment_df.to_csv("housing1.csv", encoding='utf-8')
    