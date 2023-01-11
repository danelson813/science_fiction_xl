import requests
from bs4 import BeautifulSoup as bs
# import xlsxwriter
import pandas as pd
from openpyxl import Workbook


url = "http://www.worldswithoutend.com/lists_sf_masterworks.asp"

COLUMN_NAMES = ['Book', 'Author', 'Year']

content = requests.get(url) 
soup = bs(content.text, "html.parser")
books = soup.find('div', {'id': 'reportlist'}).find('table').findAll("td", {'valign':'top'})


wb = Workbook()
ws = wb.active
ws.title = 'books_sheet1'

ws.append(COLUMN_NAMES)

for book in books:
    try:
        title = book.find('p', class_='title').text
    except:
        continue
    try:
        author = book.find('p', class_='author').text
    except:
        continue
    try:
        year = book.find('td', class_='small').text.split('(')[1][:-2]
    except:
        continue
    ws.append([title, author, year])


wb.save("SF Masterworks2.xlsx")

df = pd.read_excel("SF Masterworks2.xlsx")
print(df.tail())