import os
import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options as FoxOptions
from selenium.webdriver.chrome.options import Options as COptions

start_time = time.time()

def is_downloaded(driver):
    try:
        r=driver.find_element_by_id('sp_1_register_pager')
        if(r.text==''):
            return False
    except:
        return False
    return True


def download_selenium(browser, way_to_files, show_browser, opt):
    browser=browser.lower()
    if(browser!="firefox" and browser!="chrome"):
        print("no browser with this name")
        return
    url = "http://register.ndda.kz/register.php/mainpage/reestr/lang/ru"
    dele=os.listdir(way_to_files)
    for delet in dele:
        os.remove(way_to_files+"\\"+delet)
        time.sleep(2)
    if(browser=="firefox"):
        options = FoxOptions()
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
    if(browser=="firefox"):
        driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path=path)
    else:
        driver=webdriver.Chrome(chrome_options=options, executable_path=path)
    driver.get(url)
 
    s_continue = driver.find_element_by_name('yt0')
 
    select = Select(driver.find_element_by_name('ReestrTableForNdda[reg_period]'))
    select1 = Select(driver.find_element_by_name('ReestrTableForNdda[reg_type]'))
    select.select_by_visible_text(opt)
    select1.select_by_visible_text('ЛС')
    s_continue.click()

    s_download=driver.find_elements_by_class_name('btn ')
    s_download[0].click()
    print('downloading in process')

    if(browser=="firefox"):
        driver1 = webdriver.Firefox(options=options, firefox_profile=profile, executable_path=path)
    else:
        driver1 = webdriver.Chrome(chrome_options=options, executable_path=path)
    driver1.get(url)
 
    s_continue = driver1.find_element_by_name('yt0')
 
    select = Select(driver1.find_element_by_name('ReestrTableForNdda[reg_period]'))
    select1 = Select(driver1.find_element_by_name('ReestrTableForNdda[reg_type]'))
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


def parse_selenium(browser,show_browser,opt1,opt2,number_of_pages=-1):
    browser=browser.lower()
    if(browser!="firefox" and browser!="chrome"):
        print("no browser with this name")
        return
    url = "http://register.ndda.kz/register.php/mainpage/reestr/lang/ru"
    if(browser=="firefox"):
        options = FoxOptions()
        path=r"D:\Users\User\Downloads\geckodriver\geckodriver.exe"
    else:
        options=webdriver.ChromeOptions()
        path=r"D:\Users\User\Downloads\ChromeDriver\chromedriver.exe"


    if(show_browser==True):
        options.add_argument("--headless")
    if(browser=="firefox"):
        driver = webdriver.Firefox(options=options, executable_path=path)
    else:
        driver=webdriver.Chrome(chrome_options=options, executable_path=path)
    driver.get(url)
 
    s_continue = driver.find_element_by_name('yt0')
 
    select = Select(driver.find_element_by_name('ReestrTableForNdda[reg_period]'))
    select1 = Select(driver.find_element_by_name('ReestrTableForNdda[reg_type]'))
    select.select_by_visible_text(opt1)
    select1.select_by_visible_text(opt2)
    s_continue.click()
    bool=False
    while(bool==False):
        bool=is_downloaded(driver)
    final_json={}
    if(number_of_pages<0):
        number_of_pages=int(driver.find_element_by_id("sp_1_register_pager").text)
    for j in range(number_of_pages-1):
        s_download=driver.find_elements_by_tag_name('td')
        old_value=s_download[24].get_attribute("title")
        n=(len(s_download)-35)/11
        print("page ",j+1," parsing start")
        for i in range(100):
            index=s_download[24+i*23].get_attribute("title")
            if(index not in final_json.keys()):
                final_json[index]={}
                final_json[index]['Тип']=s_download[25+i*23].get_attribute("title")
                final_json[index]['Торговое название']=s_download[26+i*23].get_attribute("title")
                final_json[index]['Вид']=s_download[27+i*23].get_attribute("title")
                final_json[index]['Дата рег.']=s_download[28+i*23].get_attribute("title")
                final_json[index]['Срок']=s_download[29+i*23].get_attribute("title")
                final_json[index]['Дата истечения']=s_download[30+i*23].get_attribute("title")
                final_json[index]['Производитель']=s_download[31+i*23].get_attribute("title")
                final_json[index]['Страна']=s_download[32+i*23].get_attribute("title")
                final_json[index]['Классификация ЛС/ИМН']=s_download[33+i*23].get_attribute("title")
                if(s_download[34+i*23].get_attribute("title")!="Нет данных"):
                    final_json[index]['МНН']=s_download[34+i*23].get_attribute("title")
                else:
                    final_json[index]['МНН']=""
                if(s_download[35+i*23].get_attribute("title")!="(0) Нет данных"):
                    final_json[index]['АТХ классификация']=s_download[35+i*23].get_attribute("title")
                else:
                    final_json[index]['АТХ классификация']=""
                final_json[index]['Лек. форма']=s_download[36+i*23].get_attribute("title")
                final_json[index]['Форма выпуска']=s_download[37+i*23].get_attribute("title")
                final_json[index]['Срок хранения']=s_download[38+i*23].get_attribute("title")
                final_json[index]['GMP']=s_download[39+i*23].get_attribute("title")
                final_json[index]['Генерик']=s_download[40+i*23].get_attribute("title")
                final_json[index]['Рецепт']=s_download[41+i*23].get_attribute("title")
                final_json[index]['Контроль']=s_download[42+i*23].get_attribute("title")
                final_json[index]['Торг. марка']=s_download[43+i*23].get_attribute("title")
                final_json[index]['Патент']=s_download[44+i*23].get_attribute("title")
                final_json[index]['Тип НД']=s_download[45+i*23].get_attribute("title")
                final_json[index]['№ НД']=s_download[46+i*23].get_attribute("title")
        driver.find_element_by_id("next_register_pager").click()
        print("page ",j+1," parsing finished")
        bool=False
        while(bool==False):
            try:
                new_value=driver.find_elements_by_tag_name('td')[24].get_attribute("title")
                if(new_value!=old_value and new_value!=''):
                    bool=True
            except:
                continue
    print("--- %s seconds ---" % (time.time() - start_time))
    driver.close()
    return(final_json)


way_to_files=r"C:\Users\User\source\repos\TestParser\Files"
file=open("data.json","w", encoding="utf-8")
#download_selenium("chrome", way_to_files, True,"Все")
parser=parse_selenium("firefox", True ,"Действующие","ЛС",4)
json.dump(parser, file, ensure_ascii=False, indent=4)
parser=parse_selenium("firefox", True ,"Действующие","МИ",4)
json.dump(parser, file, ensure_ascii=False, indent=4)
