import json
import requests
import shutil
import time
import os
 
#This file gets all the images from the saved urls from ebay and uses request to get url and download images and move them 
#to proper folder

#Then for the next item it overwrites previous images and deletes the old extra images

#Upon program ending with 'q' input, all photos are erased
DATA_FILE="data.json" 

global img, img_prev
img =0
img_prev=0
source = r'C:\Users\username\Downloads\ebysave\image'
destination = r'C:\Users\username\Downloads\ebysave\post_images\image'
with open(DATA_FILE) as json_file:
    data = json.load(json_file)
    while 1:
        print("\n")
        img_prev = img
        value=input("(Enter 'q' to quit) What index:")
        time.sleep(1)
        if(value == 'q'):
            for i in range(img_prev):
                os.remove(destination + str(img_prev-i)+".jpg")
            break
        for i in range(len(data["ebay_list"])):
            if(int(value) == i):
                print("\n")
                print(data["ebay_list"][i]['Title'] + "\n")
                print(data["ebay_list"][i]['Price'], "\n")
                print(data["ebay_list"][i]['Part num'] + "\n")
                print(data["ebay_list"][i]['Description'] + "\n")
                for k in range(12):
                    url= data["ebay_list"][i]['Pic'+str(k+1)]
                    if url != "null":
                        response= requests.get(url)
                        if response.status_code == 200:
                            with open("image"+str(k+1)+".jpg", 'wb+') as f:
                                f.write(response.content)
                            time.sleep(2)
                            img = k+1
                            shutil.move(source + str(img)+".jpg", destination + str(img)+".jpg")
                    else:
                        break
        if(img < 12 and img != img_prev):
            for i in range(img_prev-img):
                os.remove(destination + str(img+(abs(img_prev-img))-i)+".jpg")
