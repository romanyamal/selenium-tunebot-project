import time 
import json
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import ElementNotInteractableException

def write_json(data, filename='data.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent = 4)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
global driver


driver= webdriver.Chrome(options=options)
driver.maximize_window()
time.sleep(0.5)
link = "https://www.ebay.com/sh/lst/ended?status=UNSOLD_NOT_RELISTED"
driver.get(link)
time.sleep(60)
search_box = driver.find_element_by_tag_name("input")
search_box.send_keys("usr")
search_box.submit()
search_box = driver.find_element_by_id("pass")
search_box.send_keys("pass")
search_box.submit()

def check_exists(driver,name):
    try:
        driver.find_element_by_class_name(name).click
        driver.find_element_by_class_name(name).click
    except ElementNotInteractableException:
        print("false")
        return False
    print("true")
    return True

def getLinks(driver,link):
    driver.get(link)
    arrylinks=[]
    results= driver.find_elements_by_partial_link_text("Relist")
    for result in results:
        arrylinks.append(result.get_attribute('href')) 
    print(arrylinks.pop(0))
    print(arrylinks.pop(0))
    return arrylinks

def ebayPro(driver, arrylinks, offset):
    item_array=[None]*17
    imagearry=[None]*20
    for i in range(len(arrylinks)): #len(arrylinks)
        for j in range(17):
            item_array[j]= "null"
        #if(i>0):
        driver.get(arrylinks[i]) #arrylinks[i]
        time.sleep(3)
        title = driver.find_element_by_name("title")
        item_array[0]=title.get_attribute("value")
        price = driver.find_element_by_name("binPrice")
        item_array[1]=price.get_attribute("value")
        partNum = driver.find_element_by_name("_st_Manufacturer Part Number")
        item_array[2]= partNum.get_attribute("value")
        description = driver.find_element_by_name("description")
        item_array[3]= description.get_attribute("value")
        iframe= driver.find_element_by_name("uploader_iframe")
        driver.switch_to.frame(iframe)
        time.sleep(0.3)
        driver.find_element_by_xpath("/html/body/div[2]/span/div[1]/form/div[2]/div[1]/div[1]/div[4]/span/span[2]").click() ##issues getting image urls, cant find span that enlarges images so full image url can be accessed
        time.sleep(0.1)
        driver.find_element_by_xpath("/html/body/div[2]/span/div[1]/form/div[2]/div[1]/div[1]/div[4]/span/span[3]").click()
        driver.switch_to.default_content()
        source= driver.find_element_by_xpath("/html/body/div[16]/div/div/div/div/img").get_attribute("src")
        for j in range(13):
            time.sleep(0.05)
            imagearry[j]= driver.find_element_by_xpath("/html/body/div[16]/div/div/div/div/img").get_attribute("src")
            arrow = driver.find_element_by_class_name("arrow-right")
            if(arrow.is_displayed()):
                arrow.click()
            else:
                print("Dosent exist, Item only has one image, item: ", i)
            if(j>0 and imagearry[j] == source):
                imagearry[j] = None
                break
            else:
                item_array[j+4]= imagearry[j]
                print(imagearry[j])
        item_array[16] = i + (offset+1)
        with open('data.json') as json_file:
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

def more_left(all_links, done):
    leftover=[None]*(len(all_links)-(done+1))
    for i in range(len(all_links)):
        if(i > done):
            leftover[i-(done+1)]= all_links[i]
    return leftover

left=[]  
left=more_left(all_links, 223)

ebayPro(driver, left, 223)
