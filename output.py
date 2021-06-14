import json

DATA_FILE="data.json"

with open(DATA_FILE) as json_file:
    data = json.load(json_file)
    while 1:
        print("\n")
        value=input("(Enter 'q' to quit) What index:")
        if(value == 'q'):
            break
        for i in range(len(data["ebay_list"])):
            if(int(value) == i):
                print("\n")
                print(data["ebay_list"][i]['Title'] + "\n")
                print(data["ebay_list"][i]['Price'], "\n")
                print(data["ebay_list"][i]['Part num'] + "\n")
                print(data["ebay_list"][i]['Description'] + "\n")
                print(data["ebay_list"][i]['Pic1'])
                print(data["ebay_list"][i]['Pic2'])
                print(data["ebay_list"][i]['Pic3'])
                print(data["ebay_list"][i]['Pic4'])
                print(data["ebay_list"][i]['Pic5'])
                print(data["ebay_list"][i]['Pic6'])
                print(data["ebay_list"][i]['Pic7'])
                print(data["ebay_list"][i]['Pic8'])
                print(data["ebay_list"][i]['Pic9'])
                print(data["ebay_list"][i]['Pic10'])
                print(data["ebay_list"][i]['Pic11'])
                print(data["ebay_list"][i]['Pic12'])
    
