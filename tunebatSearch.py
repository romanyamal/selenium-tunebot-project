import time
import numpy
from scipy import stats
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import pandas as pd

#driver = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
global driver

def searchparty(search):
    global driver
    driver= webdriver.Chrome(options=options)
    driver.maximize_window()
    link = 'https://tunebat.com/'
    driver.get(link)
    search_box = driver.find_element_by_name('q')
    search_box.send_keys(search)
    search_box.submit()
    driver.implicitly_wait(0.5)
    result=driver.find_element_by_class_name("search-link").get_attribute('href')
    driver.get(result)
    print(result)
    driver.implicitly_wait(1.5)
    allitems=driver.find_elements_by_class_name("detailedTrackNode")
    array2d=[['Song name', 'Artist','Camelot','BPM','Popularity','Energy','Danceablity','Happiness']]
    temp=[]
    camelot=[]
    bpm=[]
    popularity=[]
    energy=[]
    danceability=[]
    happiness=[]
    #Aquilo\nSilhouette\n3B\n78\n66\n41\n23\n14
    #['Aquilo', 'Silhouette', 3B, 78, 66, 41, 23, 14]
    for i in range(len(allitems)):
        if(allitems[i].text != ''):
            temp=(allitems[i].text).split('\n')
            move=temp[1]
            temp[1]=temp[0]
            temp[0]=move
            array2d.append(temp)
            camelot.append(array2d[i][2])
            bpm.append(array2d[i][3])
            popularity.append(array2d[i][4])
            energy.append(array2d[i][5])
            danceability.append(array2d[i][6])
            happiness.append(array2d[i][7])
            time.sleep(0.01)
            print(i,  " " ,  array2d[i]) #, camelot[i], bpm[i], popularity[i], energy[i], danceability[i], happiness[i]
    camelot.pop(0)
    #print(array2d)
    print(numpy.mean(camelot))
name = input("Enter song name and artist:")
#time.sleep(8)
if(name == ''):
    name = "atlantis seafret"
    
searchparty(name)

time.sleep(5) # Let the user actually see something!
driver.close()
