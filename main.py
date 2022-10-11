import xlrd
import time
import datetime
from datetime import datetime
import ujson
from tqdm import tqdm

print("Wczytywanie pliku Biblioteka.xls")
time.sleep(2)
try:
    wb = xlrd.open_workbook("Biblioteka.xls")
    ws = wb.sheet_by_index(0)
    print("Pomyślnie wczytano plik 'Biblioteka.xls'")
    print("Znaleziono: ", int(ws.nrows), "pozycji." )
except:
    print("Nie można odczytać pliku 'Biblioteka.xls'")
    input("Press Enter to continue...")
    exit()
books=int(0)
invalid_books = []
print("Generowanie pliku .json...")

ts = time.time()
timestamp = ts
date_time = datetime.fromtimestamp(timestamp)
archive = str("Books") + "_" + date_time.strftime("%d_%m_%Y_%H_%M") +".json"

with open(archive, 'w', encoding='utf8') as f:
    print("Plik .json został utworzony w:", archive)
filename = archive
lst = []
time.sleep(1)
for i in tqdm(range(ws.nrows)):
    lock = 0
    if ws.cell_value(i,5) == "":
            barcode=int(ws.cell_value(i,0))
            try:
                title=str(ws.cell_value(i,1))
                signature=str(ws.cell_value(i, 2))
                try:
                    price=float(ws.cell_value(i, 3))
                except:
                    price=float(0)
                try:
                    book_value=float(ws.cell_value(i, 4))
                except:
                    book_value=float(0)
                if ws.cell_value(i, 6) == "Tak":
                    pre_demonetization = "True"
                else:
                    pre_demonetization ="False"
            except:
                if lock == 0:
                    print("")
                    print("Książka o numerze: ", barcode, "sprawia problem, proszę zobaczyć plik .xls. Nieparwidłowe pozycje zostaną zastąpione 0")
                    invalid_books.append(barcode)
                    lock = 1

            with open(filename, mode='w') as f:
                ujson.dump(lst, f)
            with open(filename, mode='w') as f:
                lst.append({'barcode': barcode,
                        'title': title,
                        'signature': signature,
                        'price': price,
                        'value': book_value,
                        'pre_demonetization': pre_demonetization,
                            })
                ujson.dump(lst, f, indent=2, ensure_ascii=False)
            books=books+1


print("Pomyślnie utworzono bazę danych książek.")
if len(invalid_books) > 0:
    print("W trakcie generowania bazy danych program napotkał się na parę problmów...")
    print("Proszę zerknąć na książki o tych numerach ID: ")
    print(*invalid_books, sep="\n")
print(books)
print((ws.nrows) - books)
input("Press Enter to continue...")
