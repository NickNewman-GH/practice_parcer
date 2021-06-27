# Парсер
Как работает программа:
1. После запуска скрипта на вход ему передаётся интервал запуска в секундах. Скрипт отработает в момент запуска и будет ждать указанный интервал до следующего запуска.
2. С реестра ЛС и МИ Казахстана выкачиваются данные в формате xls. Т. к чтобы получить весь реестр по ЛС и МИ нужны два отдельных запроса, то файлов получается два. Скачивание происходить асинхронно в два потока для увеличения скорости. 
3. Поочерёдно считываем данные с каждого из полученных файлов, проверяя записи на уникальность и записывая их в словарь, соблюдая нужную нам структуру json файла. 
4. Сохраняем полученный словарь в формате json. 
5. Скрипт ждёт указанный интервал времени и повторяет шаги 2-4. 

Требования:

*Использованы сторонние библиотеки:
1. xlrd
2. requests 

Примерное время и процесс работы программы:
```
--- start downloading data_LSs.xls ---
--- start downloading data_MIs.xls ---
--- data_MIs.xls download is complete! it took 146.26184964179993 seconds  ---
--- data_LSs.xls download is complete! it took 159.09277081489563 seconds  ---
--- parsing begins ---
--- parsing complete in 8.639833450317383 seconds ---
--- entries parsed = 47564 ---
--- saving in json format ---
--- saving complete in 6.376640796661377 seconds ---
--- total time 174.1092450618744 seconds ---
```
# Парсер на "selenium"
Как работает программа:

Примерное время работы программы:
