import xlrd
import requests
import json
import html
import time
from multiprocessing.pool import ThreadPool

start_time = time.time()

def download_xls(params):
    type,filename = params
    table_url = 'http://register.ndda.kz/register.php/mainpage/reestr/lang/ru'
    load_url = 'http://register.ndda.kz/register.php/mainpage/exportRegister'

    data={'ReestrTableForNdda[reg_type]': type, 'ReestrTableForNdda[reg_period]': 0}

    session.post(table_url, data=data)
    response = session.get(load_url)
    data = response.content

    with open(filename, 'wb') as file:
        file.write(data)
    return filename

def get_col_names(sheet):
    col_names = []
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        for i in range(2,len(row)):
            col_names.append(row[i].strip())
        break
    return col_names

def process_string_data(string):
    result = string.strip()
    result = result.replace('\n','')
    result = html.unescape(result)
    return result

def parse_xls(files_to_parse):
    #открываем файлы
    docs = []
    for f in files_to_parse:
        docs.append(xlrd.open_workbook(f,ignore_workbook_corruption=True))
    
    col_names = []
    parsed_data = {}

    #обработка файлов
    for doc in docs:

        sheet = doc.sheet_by_index(0)
        #заполняем массив имен
        if len(col_names) == 0:
            col_names = get_col_names(sheet)
            
        #парсим таблицу
        for rownum in range(1,sheet.nrows):
            row = sheet.row_values(rownum)
            parsed_data[row[1]] = dict()
            
            for i in range(2,len(row)):
                #если строка, приводим в нормальный вид
                if(isinstance(row[i],str)):
                    cell = process_string_data(row[i])
                else:
                    cell = row[i] 
                parsed_data[row[1]][col_names[i-2]] = cell
                
    return parsed_data

if __name__ == '__main__':
    files_to_parse = []
    #скачиваем файлы
    
    with requests.Session() as session:
        types = [(1,'data_LSs.xls'), (2, 'data_MIs.xls')]
        downloaded_files = ThreadPool(len(types)).imap_unordered(download_xls, types)

        
        for file in downloaded_files:
            print(file,"--- %s seconds ---" % (time.time() - start_time))
            files_to_parse.append(file)
            
    

    parsed_data = parse_xls(files_to_parse)
            
    jout = open('KZ.json','w', encoding='utf8')
    json.dump(parsed_data,jout,ensure_ascii=False, indent=4)
    jout.close()
            
    print('entries parsed - ',len(parsed_data))
    
    print('parsing complete',"--- %s seconds ---" % (time.time() - start_time))
