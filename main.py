from bs4 import BeautifulSoup
import requests
import random
import pandas as pd 
import numpy
from lxml import etree
import json
import time



df = pd.read_csv('Amazon Scraping - Sheet1.csv')

data_dict = df.to_dict('list')

#print(*data_dict)

asin_lst = data_dict['Asin']
country_lst = data_dict['country']

print('Data Readed Sucessfully')

output_format = {}
final_lst = []

product_detail = {}


count = 0

print("Please Wait....")
print("Note :- Please don't stop the program JSON file will be created at the last if you will stop it you will not get JSON File")

start = time.time()

for i in range(0,1000):
    
    country = country_lst[i]
    asin = asin_lst[i]
    URL = "https://www.amazon.{}/dp/{}".format(country,asin)


    HEADERS = ({'User-Agent':
			'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
			(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
			'Accept-Language': 'en-US, en;q=0.5'})
    
    
        
    if (i == count*100):
        end = time.time()
        if i-100 < 0 :
            num = 0
        else:
            num = i-100
        msg = f"Runtime of the program at {num} to {count*100} is {end - start}\n"
        with open("time_output.txt", "a") as outfile:
            outfile.write(msg)
        start = time.time()
        
    if i%100 == 0:
        count+=1

   
   
    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")
    dom = etree.HTML(str(soup))
    
   
  
    
    try:  
        product_title = dom.xpath('//*[@id="productTitle"]')[0].text
        product_title = product_title.strip()
        output_format['Product_title'] = product_title
        images = soup.find('img',{'id':"imgBlkFront"})
        
        output_format['Product_img_url'] = images['src']
    except:
        pass
    
    if country == 'fr':
        
        try:   
            price = soup.find('span',{"class":"a-color-base"})
            price = price.text
            p
            price = price.lstrip()
            
            output_format['Product_price'] = price
        except:
            pass
    else:
        try:   
            price = soup.find('span',{"class":"a-size-base a-color-price a-color-price"})
            price = price.text
            price = price.lstrip()
            
            output_format['Product_price'] = price
        except:
            pass
    try:
        product_details = soup.find('div',{'id':'detailBullets_feature_div'})
        product_details = product_details.findAll('span')
        lst = []
        clean_lst = []
        for detail in product_details:
            d = detail.text.replace('\n',"")
            lst1 = (d.replace('\u200f',"")).replace('\u200e',"").strip().split(":")
            #print(lst1)
            for j in lst1:
                if j == '':
                    pass
                else:
                    lst.append(j.strip())
    
   
        
        
        for ele in lst:
            if ele in clean_lst:
                pass
            else:
                clean_lst.append(ele)
        
        
    
        product_detail[clean_lst[0]] = clean_lst[1]
        product_detail[clean_lst[2]] = clean_lst[3]
        product_detail[clean_lst[4]] = clean_lst[5]
        product_detail[clean_lst[6]] = clean_lst[7]
        product_detail[clean_lst[8]] = clean_lst[9]
        
    except:
        pass
    
        
    
        
    
    if output_format == {}:
        pass
    else: 
        output_format['Product_details'] = product_detail
        # print(output_format)
        json_object = json.dumps(output_format, indent=4)
        
        
        
        final_lst.append(output_format)
        
        
    
    output_format = {}
    product_detail = {}
    
#print(final_lst)

json_object = json.dumps(final_lst, indent=4)
with open("sample.json", "w") as outfile:
    outfile.write(json_object)
    print('Data Successfully Created..')


    

   


