
import urllib.request
import urllib.parse
from urllib.parse import urlparse
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import os, subprocess, threading, sys
from os import rename, listdir

#from win32_setctime import setctime
from datetime import datetime 
import time

import csv



band_home = "https://band.us/band/"
band_id = "48320017"  #돼지기술공감

#dn_root = 'D:/band/'
#bandvideo = 'BandVideo.mp4'




def main():
    #chrome_driver = './chromedriver_103_0_5060.exe'
    chrome_driver = 'D:/Project/GIT/BandCrawling/BandCrawling/chromedriver_103_0_5060.exe'
    options = Options()
    options.headless = False

    driver = webdriver.Chrome(executable_path=chrome_driver, options=options)
    driver.implicitly_wait(3)


    driver.get("https://auth.band.us/login_page")

    time.sleep(1)

    global band_id
    driver.get(band_home + band_id)
    #driver.get(https://band.us/band/48320017)
    time.sleep(1)
    
    #다 저장한 후에 텍스트에서 열어서 UTF-8(BOM)으로 저장해야 글씨가 안깨짐
    f = open("write{0}.csv".format(datetime.now().strftime('%Y-%m-%d_%H%M%S')),'w', newline='', encoding='UTF-8')
    wr = csv.writer(f)

    prevData = ""
    prevDataCnt = 0

    indexCnt = 0
    while True : 
        indexCnt += 1
        try :
            timetag = driver.find_element("xpath", '//*[@id="wrap"]/div[2]/div/div/section/div[2]/div/section/div/div[2]/div/div/a')
            timeT = timetag.text
            
            idx = timeT.index("일")
            timeT = timeT[0:idx + 1]

            timeT = timeT.replace(" ", "")
            timeT = timeT.replace("년", "-")
            timeT = timeT.replace("월", "-")
            timeT = timeT.replace("일", "")

            

            data = driver.find_element("xpath", '//*[@id="wrap"]/div[2]/div/div/section/div[2]/div/section/div/div[3]')
            textLine = data.find_elements(By.CLASS_NAME, "dPostTextView")
            
            strData = ""
            for e in textLine :
                strData = strData + e.text + "\n"

            #이전 데이터와 동일하면 패스
            if prevData == strData :
                prevDataCnt += 1

                if prevDataCnt == 10 :      # 다시한번 다음 버튼클릭!
                    driver.find_element("xpath", '//*[@id="wrap"]/div[2]/div/div/section/button[3]').click()    #다음버튼 클릭
                    time.sleep(2)

                elif prevDataCnt == 15 :    # 너무 안바뀌면 종료!
                    break

                continue
                
            
            print(strData)
            prevData = strData
            prevDataCnt = 0

            wr.writerow([timeT, strData])
            #time.sleep(1)

            driver.find_element("xpath", '//*[@id="wrap"]/div[2]/div/div/section/button[3]').click()    #다음버튼 클릭
            time.sleep(2)

        except Exception as e :
           print(e)
    
    f.close()

    return


##############################################################################################################################
#여기서부터 시작

if __name__ == "__main__":  
    main()

