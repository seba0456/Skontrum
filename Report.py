import time
from datetime import datetime
import ujson
from tqdm import tqdm
a = 1

def excel_headers ():
    worksheet.write(0, 0, "Numer inwenterażowy")
    worksheet.write(0, 1, "Tytuł")
    worksheet.write(0, 2, "Sygnatura")
    worksheet.write(0, 3, "Cena")
    worksheet.write(0, 4, "Wartość")
    worksheet.write(0, 5, "Przed denominacją?")

ts = time.time()
timestamp = ts
date_time = datetime.fromtimestamp(timestamp)

while a == 1:
    file = input("Proszę wprowadzić nazwę pliku .json zawierającego bazę książek:")
    try:
        with open(file, 'r') as f:
            distros_dict = ujson.load(f)
            a = 0
    except:
        print("Invalid file name, please try again...")
x=[]
barcodes= []
barcodes_scanned= []
for x in tqdm(distros_dict):
    barcodes.append(int(x["barcode"]))
time.sleep(1)
b=1
while b == 1:
    file_b = input("Proszę wprowadzić nazwę pliku .json zawierającego ZESKANOWANE KSIAŻKI:")
    print('―' * 30)
    print("Generowanie raportu o brakujących książkach...")
    try:
        with open(file_b, 'r+', encoding="windows-1250") as fb:
            distros_dict_b = ujson.load(fb)
            b = 0
        for x in tqdm(distros_dict_b):
            barcodes_scanned.append(int(x["barcode"]))
    except:
        print("Invalid file name, please try again...")
missing_books = []
missing_books = list(set(barcodes)-set(barcodes_scanned))
file_c = str("Missing_Books") + "_" + date_time.strftime("%d_%m_%Y_%H_%M") + ".json"

time.sleep(1)
with open(file_c, 'w', encoding='utf8') as f:
    print("Plik .json został utworzony w:", file_c)
time.sleep(1)
lst=[]
print("Trwa generowanie...")
time.sleep(0.5)
for y in tqdm(missing_books):
    for x in distros_dict:
        if x["barcode"] == y:
            title = str(x["title"])
            signature = str(x["signature"])
            price = float(x["price"])
            book_value = float(x["value"])
            pre_demonetization = str(x["pre_demonetization"])

            with open(file_c, mode='w') as f:
                ujson.dump(lst, f)
            with open(file_c, mode='w') as f:
                lst.append({'barcode': y,
                            'title': title,
                            'signature': signature,
                            'price': price,
                            'value': book_value,
                            'pre_demonetization': pre_demonetization,
                            })
                ujson.dump(lst, f, indent=2, ensure_ascii=False)
print("Plik .json dla niezeskanowanych książek został wygenerowany...")
time.sleep(1)
print('―' * 30)
print("Genreuję plik .xls...")

import xlsxwriter
file_d = str("Missing_Books") + "_" + date_time.strftime("%d_%m_%Y_%H_%M") + ".xlsx"
workbook = xlsxwriter.Workbook(file_d)
worksheet = workbook.add_worksheet()
row = 1
column = 0
excel_headers()
with open(file_c, 'r', encoding="windows-1250") as fb:
    distros_dict_c = ujson.load(fb)

for x in tqdm(distros_dict_c):
    barcode = int(x["barcode"])
    title = str(x["title"])
    signature = str(x["signature"])
    price = float(x["price"])
    book_value = float(x["value"])
    pre_demonetization = str(x["pre_demonetization"])
    worksheet.write(row, 0, barcode)
    worksheet.write(row, 1, title)
    worksheet.write(row, 2, signature)
    worksheet.write(row, 3, price)
    worksheet.write(row, 4, book_value)
    if pre_demonetization==str("True"):
        pre_demonetization=str("Tak")
    else:
        pre_demonetization = str("Nie")
    worksheet.write(row, 5, pre_demonetization)
    row += 1
workbook.close()
print('―' * 30)
print("Trwa generowanie raportu zeskanowanych książek...")
file_d = str("Scanned_Books") + "_" + date_time.strftime("%d_%m_%Y_%H_%M") + ".xlsx"
workbook = xlsxwriter.Workbook(file_d)
worksheet = workbook.add_worksheet()
row = 1
column = 0

with open(file_b, 'r', encoding="windows-1250") as fb:
    distros_dict_b = ujson.load(fb)
    excel_headers()
for x in tqdm(distros_dict_b):
    barcode = int(x["barcode"])
    title = str(x["title"])
    signature = str(x["signature"])
    price = float(x["price"])
    book_value = float(x["value"])
    pre_demonetization = str(x["pre_demonetization"])
    worksheet.write(row, 0, barcode)
    worksheet.write(row, 1, title)
    worksheet.write(row, 2, signature)
    worksheet.write(row, 3, price)
    worksheet.write(row, 4, book_value)
    if pre_demonetization==str("True"):
        pre_demonetization=str("Tak")
    else:
        pre_demonetization = str("Nie")
    worksheet.write(row, 5, pre_demonetization)
    row += 1
workbook.close()
print('―' * 30)
print("Gotowe!")
input("Press Enter to continue...")