import time
import numpy

from scipy import stats
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
global driver

driver= webdriver.Chrome(options=options)
driver.maximize_window()
time.sleep(0.5)
link = "https://www.ebay.com/sh/lst/ended?status=UNSOLD_NOT_RELISTED/"
driver.get(link)
time.sleep(0.5)
time.sleep(0.5)
time.sleep(0.5)
search_box = driver.find_element_by_tag_name("input")
search_box.send_keys("username")
search_box.submit()
search_box = driver.find_element_by_id("pass")
search_box.send_keys("password")
search_box.submit()
link="https://www.ebay.com/sh/lst/ended?status=UNSOLD_NOT_RELISTED&limit=200"
driver.get(link)

arrylinks=[]
results=driver.find_elements_by_partial_link_text("Relist")
for result in results:
    arrylinks.append(result.get_attribute('href'))
n=0
arrylinks.pop(0)
imagearry=[]
for i in range(3): #len(arrylinks)
    time.sleep(0.5)
    if(i>0):
        driver.get(arrylinks[i])
        time.sleep(2)
        title = driver.find_element_by_name("title")
        title.get_attribute("value")
        price = driver.find_element_by_name("binPrice")
        price.get_attribute("value")
        partNum = driver.find_element_by_name("_st_Manufacturer Part Number")
        partNum.get_attribute("value")
        description = driver.find_element_by_name("description")
        description.get_attribute("value")
   
        iframe= driver.find_element_by_name("uploader_iframe")
        driver.switch_to.frame(iframe)
        image = driver.find_element_by_xpath("/html/body/div[2]/span/div[1]/form/div[2]/div[1]/div[1]/div[4]/span/span[2]").click() ##issues getting image urls, cant find span that enlarges images so full image url can be accessed
        image = driver.find_element_by_xpath("/html/body/div[2]/span/div[1]/form/div[2]/div[1]/div[1]/div[4]/span/span[3]").click()
        driver.switch_to.default_content()
        source=driver.find_element_by_xpath("/html/body/div[16]/div/div/div/div/img").get_attribute("src")
        
        #need for loop to get all images
        #need if to make sure that no immage url duplicates
        driver.find_element_by_class_name("arrow-right").click()

        #figure out how to add all info to excel sheet
        
        
#working on it
driver.switch_to.default_content()
print(len(image))
for i in image:
    i.get_attribute("innerHTML")
    print(n)
    n=n+1

# iframe= driver.find_elements_by_tag_name("iframe")
print(results)
driver.implicitly_wait(1.5)
allitems=driver.find_elements_by_class_name("detailedTrackNode")

link="https://www.ebay.com/sh/lst/ended?status=UNSOLD_NOT_RELISTED"
