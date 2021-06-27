# Парсер
Файл - ```parser.py```</br></br>
Как работает программа:
1. После запуска скрипта на вход ему передаётся интервал запуска в секундах. Скрипт отработает в момент запуска и будет ждать указанный интервал до следующего запуска.
2. С реестра ЛС и МИ Казахстана выкачиваются данные в формате xls. Т. к чтобы получить весь реестр по ЛС и МИ нужны два отдельных запроса, то файлов получается два. Скачивание происходить асинхронно в два потока для увеличения скорости. 
3. Поочерёдно считываем данные с каждого из полученных файлов, проверяя записи на уникальность и записывая их в словарь, соблюдая нужную нам структуру json файла. 
4. Сохраняем полученный словарь в формате json. 
5. Скрипт ждёт указанный интервал времени и повторяет шаги 2-4. 

Требования:
* python3
   Использованы сторонние библиотеки:
   * xlrd
   * requests 

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
Файл - ```Selenium_parser.py```
Как работает программа:
1. На вход функции подаются различные данные, с помощью которых регулируются объёмы парсируемых данных(количество ячеек, запросы к сайту и т.п.) и браузер, с которого происходит заход.
2. Функция заходит на сайт с выбранного брузера, вводит в форму необходимые данные и ждёт загрузки страницы.
3. После загрузки страницы начинает считывать данные из таблицы(title элемента <td>) и заносить их в словарь(проверяя на уникальнсть ключей).
4. После сбора всей информации программа наживает на кнопку перехода на новую страницу и ждёт обновления информации.
5. действия 4-5 повторяются до конца страниц.
6. Получившийся словарь заносится в json-файл
7. Сессия закрывается
  
Из-за особенностей сайта процесс загрузки таблицы и обновления данных в ней довольно долгий, из-за чего после сравнительно долгого парсинга самой страницы нужно некоторое время ждать, пока загрузится другая страница, что делает эту программу очень долгой. Однако основной скрипт завязан на скачивании xls-файла со страницы, что может быть затруднено различными обстоятельствами. Для таких случаев можно воспользоваться парсингом через selenium
  
Требования:
1. Python 3
2. библиотеки для Python 3,перечисленные ниже
3. Браузер Google Chrome, или Mozilla Firefox
4. Драйверы для рабты с браузерами (находятся в архиве Drivers)
  
Используемые библиотеки:
1.Selenium
2.Os
3.Json
  
В качестве небольшого бонуса есть функция скачивания xls-файлов с сайта, которая открывает две сессии браузера, выставляет необходимые данные в форме, ждёт загрузки страниц, нажимает на кнопки скачивания файлов, ожидает завершения скачивания файлов и закрывает сессию.
  
Примерное время работы программы:
4 часа
