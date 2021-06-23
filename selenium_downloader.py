import shutil
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options

start_time = time.time()

def download_selenium(browser, way_to_files, show_browser, opt):
    url = "http://register.ndda.kz/register.php/mainpage/reestr/lang/ru"
    dele=os.listdir(way_to_files)
    for delet in dele:
        os.remove(way_to_files+"\\"+delet)
        time.sleep(2)
    if(browser=="firefox"):
        options = Options()
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("browser.download.manager.showWhenStarting", False)  
        profile.set_preference("browser.download.dir", way_to_files)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, application/vnd.ms-excel, text/csv, text/comma-separated-values, application/octet-stream")
        path=r"D:\Users\User\Downloads\geckodriver\geckodriver.exe"
    else:
        options=webdriver.ChromeOptions()
        prefs = {"download.default_directory" : way_to_files}
        options.add_experimental_option("prefs", prefs)
        path=r"D:\Users\User\Downloads\ChromeDriver\chromedriver.exe"


    if(show_browser==True):
        options.add_argument("--headless")
    if(browser=="Firefox"):
        driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path=path)
    else:
        driver=webdriver.Chrome(chrome_options=options, executable_path=path)
    driver.get(url)
 
    s_continue = driver.find_element_by_name('yt0')
 
    select = Select(driver.find_element_by_name('ReestrTableForNdda[reg_period]'))
    select1 = Select(driver.find_element_by_name('ReestrTableForNdda[reg_type]'))
    #select.select_by_visible_text('Все')
    select.select_by_visible_text(opt)
    select1.select_by_visible_text('ЛС')
    s_continue.click()

    s_download=driver.find_elements_by_class_name('btn ')
    s_download[0].click()
    print('downloading in process')

    if(browser=="Firefox"):
        driver1 = webdriver.Firefox(options=options, firefox_profile=profile, executable_path=path)
    else:
        driver1 = webdriver.Chrome(chrome_options=options, executable_path=path)
    driver1.get(url)
 
    s_continue = driver1.find_element_by_name('yt0')
 
    select = Select(driver1.find_element_by_name('ReestrTableForNdda[reg_period]'))
    select1 = Select(driver1.find_element_by_name('ReestrTableForNdda[reg_type]'))
    #select.select_by_visible_text('Все')
    select.select_by_visible_text(opt)
    select1.select_by_visible_text('МИ')
    s_continue.click()

    s_download=driver1.find_elements_by_class_name('btn ')
    s_download[0].click()
    time.sleep(5)
    counter=0
    while(1):
        time.sleep(1)
        counter=0
        files = os.listdir(way_to_files)
       # print(len(files))
        for file in files:
            if (file.endswith(".xls.part") or file.endswith(".crdownload")):
               # print("exist")
                counter=1
        if(len(files)==2 and counter!=1):
            break
    print("downloaded successfully")
    print("--- %s seconds ---" % (time.time() - start_time))
    driver.close()
    driver1.close()



way_to_files=r"C:\Users\User\source\repos\TestParser\Files"
download_selenium("chrome", way_to_files, True,"Все")