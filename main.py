from flask import Flask
from flask_restful import Api,Resource
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
from webdriver_manager.chrome import ChromeDriverManager
import os



app=Flask(__name__)
api=Api(app)


def playlist(playlist_url):
    playlist=playlist_url
    options1=webdriver.ChromeOptions()

        
    options1.add_argument("--headless")
    options1.add_argument("--disable-dev-shm-usage")        
    options1.add_argument('--no-sandbox')
    options1.add_argument("--disable-gpu")
    ## might not be needed
    options1.add_argument("--remote-debugging-port=9222")
    options1.add_argument('--window-size=1920x1480')
    driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=options1)
    
    youtube_all=[]
    driver.get(playlist)


    search = driver.find_elements(by=By.ID,value="video-title")
    for srch in search:
        youtube_all.append(srch.get_attribute(name="href"))
    return youtube_all

def mp3(youtube_all):
        
        options1=webdriver.ChromeOptions()

        
        options1.add_argument("--headless")
        options1.add_argument("--disable-dev-shm-usage")
        options1.add_argument('--no-sandbox')
        options1.add_argument("--disable-gpu")
        ## might not be needed
        options1.add_argument("--remote-debugging-port=9222")
        options1.add_argument('--window-size=1920x1480')
        driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=options1)

        driver.get("https://yt2mp3.tech/")



        search = driver.find_element(by=By.CLASS_NAME,value="link-form")


        for youtube in youtube_all:
            search.send_keys(youtube)
            search.send_keys(Keys.RETURN)

            try:
                main = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, "download"))
                )
                
                lnks=driver.find_elements(by=By.LINK_TEXT,value="Download")

                for lnk in lnks:
        
                    lnk.click()
                search.clear()
            except:
                driver.quit()
            time.sleep(10)


class Converter(Resource):
  
    def get(self,playlist_url):
       
        playlist_url=playlist_url.replace("jai","/")
        playlist_url=playlist_url.replace("rajani","?")
        print(playlist_url)
        youtube_all=playlist(playlist_url)
        mp3(youtube_all)
        return {"completion":"success"}
       

api.add_resource(Converter,"/convert/<string:playlist_url>")
if __name__=="__main__":
    app.run(debug=True)