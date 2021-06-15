import json
import requests
import shutil
import time
import os

DATA_FILE="partsmart15.json" 
#DATA_FILE="sepsparts.json" 

global img
img=0
source = r'C:\Users\sepsparts\Downloads\ebysave\image'
destination = r'C:\Users\sepsparts\Downloads\ebysave\post_images\image'
with open(DATA_FILE) as json_file:
    data = json.load(json_file)
    while 1:
        print("\n")
        value=input("(Enter 'q' to quit) What index:")
        time.sleep(1)
        if(img < 12 and img != 0):
            for i in range(12-img):
                os.remove(destination + str(img+i)+".jpg")
        if(value == 'q'):
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
