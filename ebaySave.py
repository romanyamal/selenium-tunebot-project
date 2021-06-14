import time 
import json
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import ElementNotInteractableException

#Constants
USERNAME = "username"
PASSWORD = "pass123"
DATA_FILE= 'data.json'

#Program designed to retrieve all ended listings data from ebay, saves data in json file
#json file: must consist of proper format like object y on line 124, all items must be inside array called "ebay_list":[]

#function to write to json file
def write_json(data, filename=DATA_FILE):
    with open(filename, 'w') as file:
        json.dump(data, file, indent = 4)

#function that checks if attribute is clickable
def check_exists(driver,name):
    try:
        driver.find_element_by_class_name(name).click
        driver.find_element_by_class_name(name).click
    except ElementNotInteractableException:
        print("false")
        return False
    print("true")
    return True

#funtion retrieves an array of links 
#drops two first links because those are not necessary
def getLinks(driver,link):
    driver.get(link)
    arrylinks=[]
    results= driver.find_elements_by_partial_link_text("Relist")
    for result in results:
        arrylinks.append(result.get_attribute('href')) 
    print(arrylinks.pop(0))
    print(arrylinks.pop(0))
    return arrylinks

#function that takes in an array and value of items completed
#then constructs an array of only uncompleted items and returns array
def more_left(all_links, done):
    leftover=[None]*(len(all_links)-(done))
    for i in range(len(all_links)+1):
        if(i > (done-2)):
            leftover[i-(done+1)]= all_links[i-1]
    leftover.pop(0)
    time.sleep(1)
    return leftover

#brains
def ebayPro(driver, arrylinks, offset):
    #create arrays of proper sizes full of null values
    item_array=[None]*17
    imagearry=[None]*20
    #for every link do this
    for i in range(len(arrylinks)): 
        #fills item_array with "null" string to clear array after every iteration
        for j in range(17):
            item_array[j]= "null"
        #open link and get attribute
        #then save attribute to item_array
        driver.get(arrylinks[i]) 
        title = driver.find_element_by_name("title")
        item_array[0]=title.get_attribute("value")
        time.sleep(0.001)
        price = driver.find_element_by_name("binPrice")
        item_array[1]=price.get_attribute("value")
        time.sleep(0.001)
        partNum = driver.find_element_by_name("_st_Manufacturer Part Number")
        item_array[2]= partNum.get_attribute("value")
        time.sleep(0.001)
        description = driver.find_element_by_name("description")
        item_array[3]= description.get_attribute("value")
        time.sleep(0.001)
        #scroll to allow the element to be in view for clicking
        driver.execute_script("window.scrollTo(0, 500)")
        #switch frames to access other code
        iframe= driver.find_element_by_name("uploader_iframe")
        driver.switch_to.frame(iframe)
        #wait to make sure page loads
        time.sleep(2)
        #access image for full size mode
        enlarge = driver.find_element_by_xpath("/html/body/div[2]/span/div[1]/form/div[2]/div[1]/div[1]/div[4]/span/span[2]") 
        invalid_photo = driver.find_element_by_xpath("/html/body/div[2]/span/div[1]/form/div[2]/div[1]/div[1]/div[1]/span/h3")
        #checks to make sure first image is valid, otherwise start from second image
        if(invalid_photo.get_attribute("innerHTML") == "Invalid photo (CLERR002)"):
            driver.find_element_by_xpath("/html/body/div[2]/span/div[1]/form/div[2]/div[3]/div/ul/li[2]/span/div[1]/img").click()
        #if images loaded click, else wait 12 seconds then click
        if(enlarge.is_displayed()):
            time.sleep(0.2)
            enlarge.click()
        else:
            time.sleep(12)
            enlarge.click()
        driver.find_element_by_xpath("/html/body/div[2]/span/div[1]/form/div[2]/div[1]/div[1]/div[4]/span/span[3]").click()
        driver.switch_to.default_content()
        time.sleep(0.5)
        #once in full size image mode get image source link for first image
        source= driver.find_element_by_xpath("/html/body/div[16]/div/div/div/div/img").get_attribute("src")
        for j in range(13):
            time.sleep(0.05)
            #add image to array
            imagearry[j]= driver.find_element_by_xpath("/html/body/div[16]/div/div/div/div/img").get_attribute("src")
            time.sleep(0.05)
            #go to next image if there is an option for next image
            arrow = driver.find_element_by_class_name("arrow-right")
            if(arrow.is_displayed()):
                arrow.click()
            else:
                print("Dosent exist, Item only has one image, item: ", i)
            #makes sure to stop after getting back to first image to avoid duplicate links
            if(j>0 and imagearry[j] == source):
                imagearry[j] = None
                break
            else:
                item_array[j+4]= imagearry[j]
                print(imagearry[j])
        #number of item from arrylinks array + offset if continuing from where left off
        item_array[16] = i + offset
        print(item_array[16])
        #add info from item_array to json object and append to file
        with open(DATA_FILE) as json_file:
            data = json.load(json_file)
            temp = data["ebay_list"]
            y={
                "Saved order": item_array[16],
                "Title": item_array[0],
                "Price": item_array[1],
                "Part num": item_array[2],
                "Description": item_array[3],
                "Pic1":item_array[4],
                "Pic2":item_array[5],
                "Pic3":item_array[6],
                "Pic4":item_array[7],
                "Pic5":item_array[8],
                "Pic6":item_array[9],
                "Pic7":item_array[10],
                "Pic8":item_array[11],
                "Pic9":item_array[12],
                "Pic10":item_array[13],
                "Pic11":item_array[14],
                "Pic12":item_array[15]
            }
            temp.append(y)
        write_json(data)

#setup selenium driver 
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
global driver

driver= webdriver.Chrome(options=options)
driver.maximize_window()
time.sleep(0.5)
#open first link
link = "https://www.ebay.com/sh/lst/ended?status=UNSOLD_NOT_RELISTED"
driver.get(link)
#sleep to give time for user to sove captcha
time.sleep(60)
#find username and password boxes and enter values
search_box = driver.find_element_by_tag_name("input")
search_box.send_keys(USERNAME)
search_box.submit()
#sleep to give time for user to sove captcha
time.sleep(60)
search_box = driver.find_element_by_id("pass")
search_box.send_keys(PASSWORD)
search_box.submit()

#combine all links from every page to all_links array
all_links=[] 
link="https://www.ebay.com/sh/lst/ended?status=UNSOLD_NOT_RELISTED&limit=200"
temp= []
temp=getLinks(driver, link)
for item in temp:
    all_links.append(item)
link="https://www.ebay.com/sh/lst/ended?status=UNSOLD_NOT_RELISTED&action=pagination&offset=200&limit=200&sort=title"
temp= []
temp=getLinks(driver, link)
for item in temp:
    all_links.append(item)
link="https://www.ebay.com/sh/lst/ended?status=UNSOLD_NOT_RELISTED&action=pagination&offset=400&limit=200&sort=title"
temp= []
temp=getLinks(driver, link)
for item in temp:
    all_links.append(item)
link="https://www.ebay.com/sh/lst/ended?status=UNSOLD_NOT_RELISTED&action=pagination&offset=600&limit=200&sort=title"
temp= []
temp=getLinks(driver, link)
for item in temp:
    all_links.append(item)
link="https://www.ebay.com/sh/lst/ended?status=UNSOLD_NOT_RELISTED&action=pagination&offset=800&limit=200&sort=title"
temp= []
temp=getLinks(driver, link)
for item in temp:
    all_links.append(item)

#only if it crashes can continue from where left off
# left=[]  
# left=more_left(all_links, 790)
# ebayPro(driver, left, 790+1)

#start the brains
ebayPro(driver, all_links, 0)
