import sys
import configparser
import os
import time

from result import Result, ResultType 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

#
# GLOBAL VARIABLE
#
name:str="Display"
version:str="v0.9.0"

driver = None

path_config:str = "./config.ini"
config = configparser.ConfigParser()

path_file:str = ''
default_display_time:int = 15

def load_config () -> Result:
    global path_file
    global default_display_time
    try :
        config.read(path_config)
        path_file = config['DISPLAY']['path_file']
        default_display_time = config['DISPLAY']['default_display_time']
        return Result(ResultType.SUCCESS, 'configuration loaded !')  
    except :
        return Result(ResultType.ERROR, 'configuration failed !') 

def sub_files (path):
    return [name for name in os.listdir(path)
        if os.path.isfile(os.path.join(path, name))]

def initialize_browser () -> Result :
    global driver
    try :
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging']);

        driver = webdriver.Chrome(chrome_options=options)
        return Result(ResultType.SUCCESS, 'browser initialized !')  
    except :
        return Result(ResultType.ERROR, 'browser initializaion failed !')  

def broswer_is_alife():
    try:
        driver.current_url
        return True
    except:
        return False

def parse_file_display_seconds(path: str) -> int :
    global default_display_time
    try :
        s = url.split('=', 1)[1].split('.', 1)[0]
        return float(s)
    except :
        #Second by default
        return float(default_display_time)

def display(url: str, seconds: int, zoom: int = 100) :
    directory = os.getcwd()
    driver.get(url)
    driver.fullscreen_window()
    driver.execute_script("document.body.style.zoom='{}%'".format(zoom))
    time.sleep(seconds)

def run ():
    global path_file
    while True:
        try :
            for file in sub_files(path_file) :
                url = path_file + file
                if(broswer_is_alife() == True):
                    seconds = parse_file_display_seconds(url)
                    if '.web' in url :
                        file = open(url, 'r')
                        for line in file.readlines() :
                            try : 
                                args = line.split('=', 2)
                                seconds = float(args[0])
                                zoom = int(args[1])
                                url = args[2]
                                print('[Display] url : {} for {} seconds'.format(url, seconds))
                                display(url, seconds, zoom)
                            except :
                                pass
                    else :
                        if '.pdf' in url :
                            url = url + '#view=Fit&toolbar=0'

                        print('[Display] url : {} for {} seconds'.format(url, seconds))
                        display(url, seconds)
                else :
                    sys.exit("[Web] Stop")
        except ValueError: 
            driver.close()
            driver.quit()
            sys.exit("[Web] " + ValueError)


if __name__ == '__main__' :
    result_lc = load_config()
    if result_lc == ResultType.ERROR : 
        print(str(result_lc))
        sys.exit()
    result_browser = initialize_browser()
    if result_browser == ResultType.ERROR : 
        print(str(result_browser))
        sys.exit()
    run()