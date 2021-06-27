#!/usr/bin/env python
import xlrd
import requests
import json
import html
import time
import os
import datetime
import sys

from multiprocessing.pool import ThreadPool

class DownloadError(Exception):
    ''' raised when an error occurs while downloading'''
    pass

class ParsingError(Exception):
    ''' raised when an error occurs while parsing'''
    pass

class InputError(Exception):
    ''' raised when user input is invalid'''

#function for downloading xls files
def download_xls(params):
    reg_type,filename = params
    table_url = 'http://register.ndda.kz/register.php/mainpage/reestr/lang/ru'
    load_url = 'http://register.ndda.kz/register.php/mainpage/exportRegister'

    data={'ReestrTableForNdda[reg_type]':reg_type, 'ReestrTableForNdda[reg_period]': 2}

    try_counter = 3
    while try_counter:
        print('--- start downloading %s ---' % filename)
        try:
            session.post(table_url, data=data)
            try:
                response = session.get(load_url)
                data = response.content
                break
            except:
                print('--- downloading %s failed ---' % filename)
                try_counter -= 1
        except:
            print('Unable to establish a connection')
            try_counter -= 1

    if not try_counter:
        return [filename,'fail']
    else:
        return [filename,data]

#function for getting the names of the colums in a spreadsheet
def get_col_names(sheet):
    col_names = []
    for rownum in range(sheet.nrows):
        row = sheet.row_values(rownum)
        for i in range(2,len(row)):
            col_names.append(row[i].strip())
        break
    return col_names

#function for processing and formatting string data
def process_string_data(string):
    null_values = ['нет данных','()']
    result = string.strip()
    result = result.replace('\n','')
    result = html.unescape(result)
    #covert all null values to empty string
    if result.lower() in null_values:
        result = ''
    return result

#function to check if an entry already exists
def identity_check(parsed_data, reg_id):
    if reg_id in parsed_data:
        return False
    return True

#function to parse binary data as xls files   
def parse_xls(files_to_parse):

    #open files as workbooks
    docs = []
    try:
        for f in files_to_parse:
            docs.append(xlrd.open_workbook(file_contents=f,ignore_workbook_corruption=True))
    except:
        raise ParsingError

    col_names = []
    parsed_data = {}

    for doc in docs:
        #get the first spreadsheet in a workbook
        sheet = doc.sheet_by_index(0)
        #get the names of the columns / keys for json
        if len(col_names) == 0:
            col_names = get_col_names(sheet)

        #parsing begins
        for rownum in range(1,sheet.nrows):
            row = sheet.row_values(rownum)
            if identity_check(parsed_data, row[1]): #check if unique
                parsed_data[row[1]] = dict()
            
                for i in range(2,len(row)):
                    #if string, then process and format
                    #else append as is
                    if(isinstance(row[i],str)):
                        cell = process_string_data(row[i])
                    else:
                        cell = row[i]
                    parsed_data[row[1]][col_names[i-2]] = cell
                
    return parsed_data

#function for saving dict in json format
def json_save(path, parsed_data):
    jout = open(path, 'w', encoding='utf8')
    json.dump(parsed_data, jout, ensure_ascii=False, indent=4)
    jout.close()

if __name__ == '__main__':

    loop_time = time.time()
    pause_time = 3 #interval between launches
    
    t_len = len(str(pause_time)) + 30

    while True:
        if pause_time - (time.time() - loop_time) < -1:
            loop_time = time.time() + 30
            print('\n!RESULTS WILL BE CLOSED IN 30 SECS!')
            while loop_time > time.time():
                continue
            os.system('cls' if os.name == 'nt' else 'clear')

        if time.time() - loop_time > pause_time:
            start_time = time.time()
    
            files_to_parse = []

            #start a session and download files asynchronously
            with requests.Session() as session:
                types = [(1,'data_LSs.xls'), (2, 'data_MIs.xls')]
                
                downloaded_files = ThreadPool(len(types)).imap_unordered(download_xls, types)
                try:
                    for filename,file in downloaded_files:
                        if file == 'fail':
                            raise DownloadError
                            
                        print('--- %s download is complete! it took %s seconds  ---' % (filename, (time.time() - start_time)))
                        files_to_parse.append(file)
                except DownloadError:
                    print("An error occured while downloading the files, script will restart later")
                    loop_time = time.time()
                    continue

            #parse dowloaded files
                
            start_time_parse = time.time()
            
            print('--- parsing begins ---')

            try:
                parsed_data = parse_xls(files_to_parse)
            except ParsingError:
                print("An error occured while parsing the files, script will restart later")
                loop_time = time.time()
                continue
            
            print('--- parsing complete in %s seconds ---' % (time.time() - start_time_parse))
            
            print('--- entries parsed = %i ---' % len(parsed_data))

            #save parsed data in json format
            
            start_time_parse_save = time.time()
            
            print('--- saving in json format ---')
            
            json_save('KZ.json', parsed_data)
            
            print('--- saving complete in %s seconds ---' % (time.time() - start_time_parse_save))
    
            print('--- total time %s seconds ---' % (time.time() - start_time))
        else:
            #display time before launch
            if pause_time - (time.time() - loop_time) > 360:
                print(('{0: <%i}' % t_len).format('%i hour(s) to start the script' % ((pause_time - (time.time() - loop_time))/360)), end='\r')
            elif pause_time - (time.time() - loop_time) > 60:
                print(('{0: <%i}' % t_len).format('%i minute(s) to start the script' % ((pause_time - (time.time() - loop_time))/60)), end='\r')
            else:
                print(('{0: <%i}' % t_len).format('%i second(s) to start the script' % (pause_time - (time.time() - loop_time))), end='\r')
