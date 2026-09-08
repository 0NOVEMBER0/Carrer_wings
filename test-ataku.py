import requests
import time

URL = "http: /127.0.0.1:8080/zapytaj"
udane=0
zablokowane=0

for numer_proby in range(1, 16):

    odpowiedz = requests.post(URL, data={"pytanie": "Cześć!"})
    print(f"Próba {numer_proby}: kod odpowiedzi {odpowiedz.status_code}")
  
    if odpowiedz.status_code==429:
        zablokowane+=1
    else:
        udane+=1

    time.sleep(7)

print(f'Udane próby ataku: {udane}')
print(f'Zablokowane próby ataku: {zablokowane}')