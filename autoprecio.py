import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://autos.mercadolibre.com.ar/volkswagen/#deal_print_id=057cdae0-1dec-11ee-ae4a-1d6fac35cf58&c_id=carousel&c_element_order=15&c_campaign=VOLKSWAGEN&c_uid=057cdae0-1dec-11ee-ae4a-1d6fac35cf58"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

#Nombres
auto = soup.find_all("a", class_="ui-search-item_groupelement shops_items-group-details ui-search-link")
autos = list()
count = 0
for au in auto:
    if count<20:
        autos.append(au.text)
    else:
        break
    count += 1

auto_precio = soup.find_all("div", class_="ui-search-item_group ui-search-itemgroup--price shops_items-group")
autos_precio = list()
count = 0
for au_precio in auto_precio:
    if count<20: 
        autos_precio.append(au_precio.text)
    else:
        break
    count += 1

autos_preciof = list()

for au_f in autos_precio:
    posicion = au_f.find("$") # Encuentra la posición del símbolo $
    parte = au_f[posicion + 1:]
    if (parte[0] == "S"):
        parte = au_f[posicion + 2:]
        autos_preciof.append(parte)
    else:
        autos_preciof.append(parte)

for auto_precio_final in autos_preciof:
    print(f"${auto_precio_final}")
