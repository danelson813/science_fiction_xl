import requests
from bs4 import BeautifulSoup as bs
import xlsxwriter
import pandas as pd


url = "http://www.worldswithoutend.com/lists_sf_masterworks.asp"

COLUMN_NAMES = ['Book', 'Author', 'Year']

content = requests.get(url) 
soup = bs(content.text, "html.parser")
books = soup.find('div', {'id': 'reportlist'}).find('table').findAll("td", {'valign':'top'})


titles = [book.find('p', class_='title') for book in books]
authors = [book.find('p', class_='author') for book in books]
years = [book.find('td', class_='small') for book in books]


workbook = xlsxwriter.Workbook("SF Masterworks.xlsx")
worksheet = workbook.add_worksheet('books_sheet')

for index, column in enumerate(COLUMN_NAMES):
    worksheet.write(0, index, column)

row_index = 1
for book in titles:
    try:
        book = book.text
        book = book.title()
    except:
        book = ""    
    worksheet.write(row_index, 0, book)
    row_index += 1

row_index = 1
for author in authors:
    try:
        author = author.text
    except:
        author = ""
    author = author.title()
    worksheet.write(row_index, 1, author)
    row_index += 1

row_index = 1
for year in years:
    try:
        year = year.text.split('(')[1][:-2]
    except:
        year = ''
    year = year.title()
    worksheet.write(row_index, 2, year)
    row_index += 1

workbook.close()


df = pd.read_excel("SF Masterworks.xlsx", names=COLUMN_NAMES)
