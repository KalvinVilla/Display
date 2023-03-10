import sys
import configparser
from result import Result, ResultType 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By

#
# GLOBAL VARIABLE
#
name:str="Display"
version:str="v0.2.0"

driver = None

path_config:str = "./config.ini"
config = configparser.ConfigParser()

path_files:str = ''
default_display_time:int = 15

def load_config () -> Result:
    global path_file
    global default_display_time
    try :
        config.read(path_config)
        path_file = config['DEFAULT']['path_files']
        default_display_time = config['DEFAULT']['default_display_time']
        return Result(ResultType.SUCCESS, 'configuration loaded !')  
    except :
        return Result(ResultType.ERROR, 'configuration failed !')  

def initialize_browser () -> Result :
    global driver
    try {
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
        try :
            s = url.split('=', 1)[1].split('.', 1)[0]
            return float(s)
        except :
            #Second by default
            return float(default_display_time)
        
def display(url: str, seconds: int) :
    directory = os.getcwd()
    driver.get(url)
    driver.fullscreen_window()
    time.sleep(seconds)

def run ():
    while True:
        try :
            for file in sub_file(path) :
                url = path + file
                if(broswer_is_alife() == True):
                    seconds = parse_file_display_seconds(url)
                    if '.web' in url :
                        file = open(url, 'r')
                        for line in file.readlines() :
                            try : 
                                args = line.split('=', 1)
                                second = float(args[0])
                                url = args[1]
                                print('[WebDisplay] url : {} for {} seconds'.format(url, second))
                                display(url, second)
                            except :
                                pass
                    else :
                        if '.pdf' in url :
                            url = url + '#view=Fit&toolbar=0'
                            
                        print('[WebDisplay] url : {} for {} seconds'.format(url, second))
                        display(url, second)
                else :
                    sys.exit("[Web] Stop")
        except : 
            driver.close()
            driver.quit()
            sys.exit("[Web] Exit error de path ")


if __name__ == '__main__' :
    define_path()
    result_lc = load_config()
    if result_lc == ResultType.ERROR : 
        print(str(result_lc))
        sys.exit()

