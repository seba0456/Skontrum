import time
import os
from datetime import datetime
import json
from tqdm import tqdm
a = 1
b = 1
c = 1
d = 1
clear = lambda: os.system('cls')
while a == 1:
    file = input("Proszę wprowadzić nazwę pliku .json zawierającego bazę książek:")
    try:
        with open(file, 'r') as f:
            distros_dict = json.load(f)
            a = 0
    except:
        print("Invalid file name, please try again...")
x=[]
barcodes= []
scanned_books=int(0)
scanned_books_list=[]
for x in tqdm(distros_dict):
    barcodes.append(int(x["barcode"]))
time.sleep(1)
print("Wczytano bazę danych książek...")
print("1.Rozpocznij nową pracę")
print("2.Wczytaj pracę")
option=int(input("Proszę wpisać numerek: "))
lst = []
if option == int(1):
    ts = time.time()
    timestamp = ts
    date_time = datetime.fromtimestamp(timestamp)
    file_b = str("Scanned_Books") + "_" + date_time.strftime("%d_%m_%Y_%H_%M") + ".json"
    with open(file_b, 'w', encoding='utf8') as f:
        print("Plik .json został utworzony w:", file_b)
    filename = file_b

elif option == int(2):
    while b == 1:
        file_b = input("Proszę wprowadzić nazwę pliku .json zawierającego ZESKANOWANE KSIAŻKI:")
        try:
            with open(file_b, 'r+',encoding='windows-1250', errors="ignore") as fb:
                distros_dict_b = json.load(fb)
                b = 0
            for x in tqdm(distros_dict_b):
                scanned_books_list.append(int(x["barcode"]))
            time.sleep(1)
            print("Wczytano plik na, którym zeskanowano: ",len(scanned_books_list), "książek.")
            scanned_books=len(scanned_books_list)
        except Exception as e: print(e)

else:
    print("Nieprawidłowa opcja, proszę uruchomić ponownie program...")
while c == 1:
    command = str(input("Wpisz komendę:"))
    if command == str("s"):
        clear()
        done=round(scanned_books/len(barcodes)*100,2)
        print("Zrobiono: ",done,"%")
        print("Proszę wprowadzić kod książki:")
        valid_book = int(0)
        try:
            value = int(input())
        except:
            print("Kod książki musi być liczbą naturalną!")
            value=int(0)
        for i in barcodes:
            if (i == value):
                if value in scanned_books_list:
                    valid_book = int(0)
                else:
                    valid_book = int(1)
        if valid_book ==int(1):
            scanned_books_list.append(int(value))
            for x in distros_dict:
                if x["barcode"] == value:
                            title = str(x["title"])
                            signature =str(x["signature"])
                            price=float(x["price"])
                            book_value=float(x["value"])
                            pre_demonetization=str(x["pre_demonetization"])
                            print(title)
            print("Pomyślnie zeskanowano książkę:", title)
            print('―' * 30)
            scanned_books = scanned_books + 1
            listObj = []
            if option==1:
                with open(file_b, mode='w') as f:
                    json.dump(lst, f)
                with open(file_b, mode='w') as f:
                    lst.append({'barcode': value,
                                'title': title,
                                'signature': signature,
                                'price': price,
                                'value': book_value,
                                'pre_demonetization': pre_demonetization,
                                })
                    json.dump(lst, f, indent=2, ensure_ascii=False)
            elif option==2:
                listObj=[]
                with open(file_b, encoding='windows-1250', errors="ignore") as fp:
                    listObj = json.load(fp)
                listObj.append({'barcode': value,
                        'title': title,
                        'signature': signature,
                        'price': price,
                        'value': book_value,
                        'pre_demonetization': pre_demonetization,
                            })
                with open(file_b, 'w', encoding='windows-1250') as json_file:
                    json.dump(listObj, json_file,
                              indent=4,
                              separators=(',', ': '),ensure_ascii=False)

                #json.dump(lst, f)

        elif valid_book==int(0):
            print("Książka została już zeskanowana, albo nie istnieje...")
    elif command == str("exit"):
        exit()
        input("Press Enter to continue...")
    elif command == str("help"):
        clear()
        print('―' * 30)
        print("Lista dostępnych komend:")
        print("s     - komenda służy do zeksanowania książki.")
        print("exit  - komenda służy do wyjścia z programu.")
        print("stat  - komenda służy do wyświetlenia statystyk.")
        print("help  - komenda służy do wyświetlenia tego komunikatu.")
        print('―' * 30)
    elif command == str("stat"):
        clear()
        print('―' * 30)
        print("Statystyki:")
        print("Zeskanowano:", scanned_books, "książek.")
        print("Pozostało:  ", (len(barcodes)-scanned_books), "książek.")
        done = round(scanned_books / len(barcodes) * 100, 3)
        print("Zrobiono:   ", done, "%.")
        print('―' * 30)
    #elif command == str("stop"):
        #Stwórz .json z niezeskanowanymi książkami
