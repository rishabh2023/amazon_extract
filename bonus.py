import cv2
import urllib.request
import easyocr
from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException
import time


URL = "https://www.amazon.com/errors/validateCaptcha"

web = webdriver.Chrome(r'C:\Program Files (x86)\chromedriver.exe')
web.get(URL)
time.sleep(5)
img = web.find_element("xpath", '/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img')
src = img.get_attribute('src')
urllib.request.urlretrieve(src, "00000001.png")
img = cv2.imread('00000001.png')
img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print('Please Wait it may make time..')
reader=easyocr.Reader(['en'])
result=reader.readtext(img,detail=0)
capdata = result[0]
capdata = capdata.replace(" ","")
print(capdata)
cap_input = web.find_element('xpath','//*[@id="captchacharacters"]')
cap_input.send_keys(capdata)
continue_btn = web.find_element('xpath','/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button')
continue_btn.click()


