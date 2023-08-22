# Тестовое задание
Реализация консольного приложения для работы с телефонной книгой с JSON файлом в качестве хранилища (phone_book.json).

## Точка входа: app.py
Консольное приложение с возможностью постраничного просмотра списка контактов, удаления, добавления, редактирования и поиска контактов по одному или нескольким критериям. Поиск осуществляется с помощью определения наличия подстроки заданного пользователем в любой части поля контакта. Модуль также содержит необходимые функции диалогов, обработки, формирования и вывода данных.

## model.py
Содержит классы Contact и ContactBook.

Класс Contact для контакта (записи в телефонной книге) реализован на основе Data classes для упрощенной инициализации и описания аннотированных полей. В нем переопределены dunder методы __str__, __dict__ (для последующей записи в JSON файл) и __post_init__ (для указания _id контакта в том случае, если создается новый контакт). 
Также реализованы методы: геттер и сеттер для _id контакта, получения полного имени контакта, вывода карточки контакта с порядковым номером, а также статический метод для проверки корректности номера телефона.

Рабочий номер вида: 909090, либо +97079090099, либо 69009009900

Класс ContactBook содержит dunder методы __init__ (инициализация из файла, если он существует, иначе - пустыми значениями с записью в созданный файл), __str__, __dict__ (для записи в JSON). Также реализованы добавление, редактирование, удаление, получение информации о контакте по id; сохранение в файл, получение списка контактов, поиск по нескольким критериям в качестве методов класса.

## generate_data.py
Генерация сотни контактов (без отчеств) для хранилища (phone_book.json).

## dialog.py
Модуль содержит функции для получения необходимой информации от пользователя через консоль, не требующие при этом создания экземпляров реализованных классов. Принцип: запрос ввода с поясняющими сообщениями; в случае запроса номера ввод осуществляется до тех пор, пока не будут получены корректные данные.

Модули задокументированы, типы имеют аннотации. 

Пример содержимого консоли во время работы программы:

Action menu: \
q - quit \
l - contact list \
a - add new contact \
r - remove a contact \
e - edit a contact \
s - search \
\
Type command and press Enter \
:l \
\
Contact List------------------------ \
Page 1/25 \
Contact card: 1 \
Full name: Tammy Alexander \
Company: Davis PLC \
Work: 101153 \
Mobile: +00597972121 \
\
Contact card: 2 \
Full name: Megan Gordon \
Company: Brown PLC \
Work: 71918904814 \
Mobile: +75433780810 \
\
Contact card: 3 \
Full name: Matthew Mckinney \
Company: Bennett, Brown and Matthews \
Work: 21832051824 \
Mobile: +70640242427 \
\
Contact card: 4 \
Full name: Blake Hughes \
Company: Simpson-Aguilar\
Work: 77079278744 \
Mobile: 12661817643 \
\
Navigation: \
b - back \
p - previous page \
n - next page \
\
Action menu: \
q - quit \
l - contact list \
a - add new contact \
r - remove a contact \
e - edit a contact \
s - search \
\
Type command and press Enter \
:s \
\
Search:----------------------------- \
Press Enter to skip\
Enter first name: \
Enter last name: \
Enter patronymic: \
Enter company name: Brown  \
Enter work number: \
Enter mobile number: + \
\
Contact List------------------------ \
Page 1/1\
Contact card: 1 \
Full name: Megan Gordon \
Company: Brown PLC \
Work: 71918904814 \
Mobile: +75433780810 \
\
Contact card: 2 \
Full name: Matthew Mckinney \
Company: Bennett, Brown and Matthews \
Work: 21832051824 \
Mobile: +70640242427 \
\
Contact card: 3 \
Full name: Noah Martinez \
Company: Shaw, Reed and Brown \
Work: 48006704239 \
Mobile: +79043772426 \
\
Navigation: \
b - back \
p - previous page \
n - next page \
\
Action menu: \
q - quit \
l - contact list \
a - add new contact \
r - remove a contact \
e - edit a contact \
s - search \
\
Type command and press Enter \
:s