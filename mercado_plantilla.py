import requests
from bs4 import BeautifulSoup
import os 
import sys
from string import Template

def obtener_autos(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    autos = soup.find_all("a", class_="ui-search-item__group__element shops__items-group-details ui-search-link")
    autos_lista = list()
    count = 0
    for auto in autos:
        if count<20:
            autos_lista.append(auto.text)
        else:
            break
        count += 1
    return autos_lista

def obtener_precios(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    autos_precio = soup.find_all("div", class_="ui-search-item__group ui-search-item__group--price shops__items-group")
    autos_precio_lista = list()
    count = 0
    for auto_precio in autos_precio:
        if count<20: 
            autos_precio_lista.append(auto_precio.text)
        else:
            break
        count += 1
    return autos_precio_lista

def obtener_precios_finales(autos_precio_lista):
    autos_preciof = list()
    for auto_precio in autos_precio_lista:
        posicion = auto_precio.find("$") # Encuentra la posición del símbolo $
        parte = auto_precio[posicion + 1:]
        if (parte[0] == "S"):
            parte = auto_precio[posicion + 2:]
            autos_preciof.append(parte)
        else:
            autos_preciof.append(parte)
    return autos_preciof

def obtener_promedio(autos_preciof):
    promedio1 = 0
    cantidad = 0

    for auto_precio_final in autos_preciof:
        auto_precio_final = auto_precio_final.replace(".","")
        texto = int(auto_precio_final)
        promedio1 = promedio1 + texto
        cantidad += 1

    promedio2 = promedio1 / cantidad
    print(f"El promedio de precios es ${promedio2}")

url = "https://autos.mercadolibre.com.ar/volkswagen/#deal_print_id=057cdae0-1dec-11ee-ae4a-1d6fac35cf58&c_id=carousel&c_element_order=15&c_campaign=VOLKSWAGEN&c_uid=057cdae0-1dec-11ee-ae4a-1d6fac35cf58"
autos_lista = obtener_autos(url)
autos_precio_lista = obtener_precios(url)
autos_preciof = obtener_precios_finales(autos_precio_lista)

""" 
for modelo, precio in zip(modelos, precios):
    print(f"{modelo}: ${precio}") """

def plantilla(modelos,precios):
    filein = open("autos/plantilla_merc.html")
    src = Template(filein.read()) #Para leer el archivo
    for modelo, precio in zip(modelos, precios):
        D = {"modelo":modelo, "precio":precio}
        result = src.substitute(D)
        try:
            os.mkdir("mercado") #Crear carpeta
            filein2 = open("mercado/"+"Datos_au"+".html", "a") #Creando archivos
            filein2.writelines(result)
        except OSError:
            if os.path.exists("mercado"):
                filein2 = open("mercado/"+"Datos_au"+".html", "a") #Creando archivos
                filein2.writelines(result)    
    print("Guardando...")
    sys.exit()

modelos = obtener_autos(url)
precios = obtener_precios_finales(obtener_precios(url))
plantilla(modelos,precios)
