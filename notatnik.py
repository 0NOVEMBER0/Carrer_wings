import os

lista_plikow = []
nazwa_pliku = input("Podaj nazwe pliku: ")



def zapisz_do_pliku(nazwa_pliku):
    try:
        with open(nazwa_pliku, "a", encoding="utf-8") as plik:
            print("Teraz mozesz pisać: ")
            print("Pusta linia końćzy wpisywanie")
            while True:
                tekst=input()
                if tekst=="":
                    break
                plik.write(tekst+"\n")
        print(f" Zapisano dane do pliku: {nazwa_pliku}")
    except Exception as e:
        print(f" Błąd zapisu: {e}")



def obsluga_pliku(komenda):
   
    if komenda=="A":
        nazwa_pliku=input("Podaj nazwa swojej notatki: ")
        if nazwa_pliku not in lista_plikow:
            lista_plikow.append(nazwa_pliku)
            zapisz_do_pliku(nazwa_pliku)
            print(f"Dodano plik: {nazwa_pliku}")
    elif komenda=="S":
        print(lista_plikow)
    elif komenda=="R":
        nazwa_pliku=input("Podaj nazwa swojej notatki: ")
        if nazwa_pliku in lista_plikow:
            lista_plikow.remove(nazwa_pliku)
            print(f"Usunięto plik: {nazwa_pliku}")
    elif komenda=="Q":
        print("Zakończono działania z plikiem")



while True:
    odpowiedz=input("Jeżeli chcesz przerwać zajmowanie się plikami, wpisz N: ").upper()
    if odpowiedz=="N":
        break
   

    komenda = input("Podaj komende do terminala [A,S,R,Q]: ").upper()


    obsluga_pliku(komenda.upper())

    if komenda=="Q":
        break