from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup



import pandas as pd
df = pd.DataFrame()


import time
from bs2json import bs2json
df = pd.DataFrame()
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome("/Library/Google/Chrome/chromedriver",chrome_options=chrome_options)

#driver.get("https://www.amazon.in/sp?_encoding=UTF8&asin=&isAmazonFulfilled=1&isCBA=&marketplaceID=A21TJRUUN4KGV&orderID=&seller=A1TIMIKWJUWKZB&tab=&vasStoreID=%5C")
driver.get("https://www.amazon.in/sp?_encoding=UTF8&asin=&isAmazonFulfilled=&isCBA=&marketplaceID=A21TJRUUN4KGV&orderID=&seller=AX7EKEDBR2R7S&tab=&vasStoreID=")
x = driver.find_element_by_xpath('//*[@id="feedback-table"]/tbody')
#print (x.text)

#print ("&&&&&&&&&&&&&&&&&&&&&&&&&")
soup = BeautifulSoup(x.get_attribute('innerHTML'),features="html5lib")
#print(soup)

m = soup.find_all('body')
#print(m)

converter = bs2json()
json = converter.convert(m[0])

rating = []
review = []
name = []

k = 0
for i in json['body']['div']:
    #print (i.keys())
    if 'i' in i.keys():
        print (i['i']['span']['text'])
        rating.append(i['i']['span']['text'])
    elif 'div' in i.keys():
        #print ("in else")
        print (i['div'][0]['span']['text'])
        review.append(i['div'][0]['span']['text'])
        print (i['div'][1]['span']['text'])
        name.append(i['div'][1]['span']['text'])
    if k == 3:
        break
    k += 1
   
time.sleep(10)
k=0
while (k<3):
    try:
        element1 = driver.find_element_by_xpath('//*[@id="feedback-next-link"]')
        element1.click()
        time.sleep(10)

        element2 = driver.find_element_by_xpath('//*[@id="feedback-table"]/tbody')
        #print (element2.text)
        soup = BeautifulSoup(element2.get_attribute('innerHTML'))
       
        n = soup.find_all('body')
        converter1 = bs2json()
        json1 = converter1.convert(n[0])
        print ("*****************************")
        #print (json1)
        k+=1
       
        for i in json1['body']['div']:
            if 'i' in i.keys():
                if i['i']['span']['text'].split(" out")[0] != "0":
                    print ("rating")
                    print (i['i']['span']['text'])
                    rating.append(i['i']['span']['text'])
            else:
                #print (i['div'][1]['span']['text'].split("on ")[1])
                if i['div'][0]['div']['span'][0]['span'][-1]['text'] not in ["template-expanded-text","emplate-response-expanded-text"]:
                    print ("review")
                    print (i['div'][0]['div']['span'][0]['span'][-1]['text'])
                    review.append(i['div'][0]['div']['span'][0]['span'][-1]['text'])

                if i['div'][1]['span']['text'].split("on ")[1] not in ["template-date.","template-response-date."]:
                    #print ("********")
                    print ("name")
                    #print (i['div'][1]['span']['text'].split("on ")[1])
                    print (i['div'][1]['span']['text'])
                    name.append(i['div'][1]['span']['text'])

    except:
       
        df['review'] = review

