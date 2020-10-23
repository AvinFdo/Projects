#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from datetime import datetime
import pandas as pd

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options  


# In[7]:


chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")

#PATH = r'C:\Program Files (x86)\chromedriver.exe' #windows
PATH = "/usr/lib/chromium-browser/chromedriver" #ubuntu 
driver = webdriver.Chrome(PATH, options=chrome_options)


# In[8]:


try:
    listings.head()
except:
    data = [{'Suburb': 0, 'Address': 0, 'Description': 0, 'Price': 0, 'Amenities': 0, 'Type': 0, 'Date': 0, 'Insights': 0, 'Schools': 0, 'URL': 0, 'Profile': 0, "Performance": 0}] 
    listings = pd.DataFrame(data)
    
with open("suburbs.txt", "r") as file_suburbs:
    all_suburbs = eval(file_suburbs.readline())

with open("comp_suburbs.txt", "r") as file_comp_suburbs:
    comp_suburbs = eval(file_comp_suburbs.readline())
    
remaining_suburbs = list(set(all_suburbs) - set(comp_suburbs))
print(len(all_suburbs), len(comp_suburbs), len(remaining_suburbs))


# In[9]:


#Landing page for melbourne house prices
for suburba in remaining_suburbs[:5]:

    page_link = "https://www.domain.com.au/sold-listings/" + suburba + "/" 
    suburb = suburba
    driver.get(page_link)
    current_url = driver.current_url 
    for page in range(1,51):
        print("Going through page", page)
        #looping through pages of listings with a suburb

        time = datetime.now()
        #file = open("ErrorLog0.txt", "a")
        #file.write('\nRan at ')
        #file.write(str(time))
        #file2 = open("UrlLog0.txt", "a")


        if page == 1:
            pass
        else:
            try:
                driver.get(current_url + "?page=" + str(page))

            except:
                #file.write("\nGoing through pages of listings within suburbs broken at page" + str(page))
                raise

        listings_links = driver.find_elements_by_css_selector("div.css-1gkcyyc > div > a")
        for n in range(0,len(listings_links)): listings_links[n] = listings_links[n].get_attribute("href")

        for n in range(0,len(listings_links)):
            driver.get(listings_links[n])

            listing_address = listing_description = listing_price = listing_amenities = listing_property_type = listing_sold_date = listing_domain_insight = listing_schools = listing_url = 0
            print(listings.shape[0], end=' ')

            try:
                #looping through listings in a page
                try:
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="listing-details__description-button"]')))
                    driver.find_element_by_xpath('//button[@data-testid="listing-details__description-button"]').send_keys(u'\ue007')
                except:
                    print("No Readmore/ Description")
                try:
                    entire_listing = driver.find_element_by_css_selector("div.listing-details__content-container > div > div").text
                    #print(entire_listing)
                except:
                    print("No Entire Listing")
                    pass

                try:
                    listing_sold_date = driver.find_element_by_css_selector("div.listing-details__summary > div.css-s4rjyl > div > span.css-h9g9i3").text
                    #listing_sold_date = driver.find_element_by_css_selector("div.listing-details__summary-title-container > div > span.listing-details__listing-tag.is-sold.listing-details__summary-tag").text
                    #print(listing_sold_date)
                except:
                    print("No listing_sold_date")
                    pass

                try:    
                    listing_price = driver.find_element_by_css_selector("div.listing-details__summary > div.css-s4rjyl > div > div.css-1wve38g > div.css-i9gxme > div").text
                    #listing_price = driver.find_element_by_css_selector("div.listing-details__address-left-column > div").text
                    #print(listing_price)
                except:
                    print("No listing_price")
                    pass

                try:
                    listing_address = driver.find_element_by_css_selector("div.listing-details__copy-text > div").text
                    #print(listing_address)
                except:
                    print("No listing_address")
                    pass

                try:
                    listing_amenities = driver.find_element_by_css_selector("div.listing-details__summary > div.css-s4rjyl > div > div.listing-details__listing-summary-features.css-er59q5 > div").text
                    #listing_amenities = driver.find_element_by_css_selector("div.listing-details__summary-title-container > div > div.listing-details__listing-summary-features.css-er59q5 > div").text
                    #print(listing_amenities)
                except:
                    print("No listing_amenities")
                    pass

                try:
                    listing_description = driver.find_element_by_css_selector("div.listing-details__description > div.noscript-expander-wrapper.css-aeox7o > div > div > div").text
                    #print(listing_description)
                except:
                    print("No listing_description")
                    pass

                try:
                    listing_property_type = driver.find_element_by_css_selector("div.listing-details__summary > div.css-s4rjyl > div > div.css-1uvlh9e > span").text
                    #listing_property_type = driver.find_element_by_css_selector("div.listing-details__property-type-features > span").text
                    #print(listing_property_type)
                except:
                    print("No listing_property_type")
                    pass

                try:
                    listing_domain_insight = driver.find_element_by_css_selector("div.listing-details__content-container > div > div > div.css-6s4w0i > div > div > p").text
                    #print(listing_domain_insight)
                except:
                    #print("No listing_domain_insight")
                    pass

                try:
                    driver.find_element_by_xpath('//button[@data-testid="fe-co-school-catchment-view-more-link"]').send_keys(u'\ue007')
                    listing_schools = driver.find_element_by_css_selector("div.listing-details__school-catchment > div > div > section").text
                    #print(listing_schools)
                except:
                    #print("No listing_schools")
                    pass

                try:
                    building_profile = driver.find_element_by_css_selector("#__domain_group\/APP_ROOT > div > div > div:nth-child(14)").text
                    #print(building_profile)
                except:
                    #print("No building_profile")
                    pass

                try:
                    performance = driver.find_element_by_css_selector("div.listing-details__suburb-insights").text
                    #print(performance)
                except:
                    #print("No performance")
                    pass

                listing_url = driver.current_url

                data = [{'Suburb': suburb,'Address': listing_address, 
                         'Description': listing_description, 'Price': listing_price, 
                         'Amenities': listing_amenities, 'Type': listing_property_type, 
                         'Date': listing_sold_date, 'Insights': listing_domain_insight, 
                         'Schools': listing_schools, 'URL': listing_url, 'Profile': building_profile, 'Performance': performance}]

                output = pd.DataFrame(data) 
                listings = listings.append(output, ignore_index=True)

                #try:
                    #file2.write("\n" + str(listing_url))
                    #file2.write("\n" + str(entire_listing) + "\n")
                #except:
                    #pass

            except:
                print("Uncaptured Error")
                pass

        #Backsup data from each page
        listings.to_csv(suburb + "-Page-" + str(page)+ ".csv", encoding='utf-8', index=False)
        #Erases data from the df
        listings = pd.DataFrame(data)
        
        #file.close()
        #file2.close()
    comp_suburbs.append(suburba)
    with open("comp_suburbs.txt", "w") as file_comp_suburbs:
        file_comp_suburbs.write(str(comp_suburbs))  

driver.quit()


# In[10]:




