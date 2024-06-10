# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 13:03:13 2024

@author: backm
"""

from time import sleep
import random
from bs4 import BeautifulSoup
# import lxml
import requests
import pandas as pd

def parse_page(url):
    sleep(random.randrange(1, 3))
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
        "Accept": "text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}
    with requests.Session() as s:
        print(url)
        response = s.get(url, headers=header)  #
        status = response.status_code  # .ok
        print('Status ', status)
        if status != 200:
            tryouts = 0
            while tryouts < 3 and status != 200:
                sleep(random.randrange(5, 20))
                response = s.get(url, proxies="", headers=header)
                tryouts += 1
                status = response.status_code  # .ok
                print('Status ', status)
    soup = BeautifulSoup(response.content, "lxml")  # .prettify()
    return soup


def get_species(group_name, group_link):
    especies=[]
    soup = parse_page(group_link)
    trs = soup.find("div",{"class":"text"}).find_all("tr")
    for tr in trs:
        nombre=pdf=ambito=nombre_comun=ficha_descriptiva=gis=""
        tds = tr.find_all("td")
        try:
            nombre = tds[0].em.get_text()
            try:
                pdf=partialURL+tds[0].a.get("href")
            except:
                pass
            try:
                ambito=tds[1].get_text().strip()
            except:
                pass
            try:
                nombre_comun=tds[2].get_text().strip()
            except:
                pass
            try:
                ficha_descriptiva=partialURL+tds[3].a.get("href")
            except:
                pass
            try:
                gis=tds[4].a.get("href")
                if gis[0:30]=='https://www.miteco.gob.es:443/':
                    soup2=parse_page(gis)
                    gis=soup2.find("h3",{"id":"ancla2"}).next_sibling.next_sibling.a.get("href")
                    print("Subweb for gis parsed")
                gis=partialURL+gis
            except:
                pass
            especies.append((group_name, nombre, nombre_comun, ambito, pdf, ficha_descriptiva, gis))
        except:
            pass
    return especies
            


           

url='https://www.miteco.gob.es/es/biodiversidad/temas/conservacion-de-especies/especies-exoticas-invasoras/ce-eei-catalogo.aspx' #all
partialURL="https://www.miteco.gob.es"



## Fetch groups
soup = parse_page(url)
group_links = [div.a.get("href") for div in soup.find_all("div",{"class":"links-list__item-title"}) if "ce_eei" in div.a.get("href")]


species=[]
for group_link in group_links:
    group_name = group_link.split("/")[-1].split(".")[0].split("_")[-1]
    print(f"Fetching {group_link}")
    for specie in get_species(group_name, group_link):
        group_name, nombre, nombre_comun, ambito, pdf, ficha_descriptiva, gis=specie
        species.append((group_name, nombre, nombre_comun, ambito, pdf, ficha_descriptiva, gis))
        

df = pd.DataFrame(species, columns=["GRUPO", "NOMBRE", "NOMBRE_COMUN", "AMBITO", "PDF", "FICHA", "GIS"])
df.to_excel("Downloads/speciesRAW.xlsx")



