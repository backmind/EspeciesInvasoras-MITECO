# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 19:45:10 2020

@author: backm
"""
import pandas as pd
import geopandas as gpd
bbox=gpd.read_file("input/mediterranean_invspp.shp",encoding="utf8")
md=gpd.read_file("output/md.shp")
df = pd.read_excel("downloads/speciesRAW.xlsx")
df = df.fillna('') 


n_mdGRUPO = len(md.GRUPO.unique())
n_mdESPECIE = len(md.ESPECIE.unique())
n_bbGRUPO = len(bbox.GRUPO.unique())
n_bbESPECIE = len(bbox.ESPECIE.unique())
n_dfGRUPO = len(df.GRUPO.unique())
n_dfESPECIE = len(df.NOMBRE.unique())


print("Especies invasoras en España totales %s en %s grupos" % (n_dfESPECIE, n_dfGRUPO))
print("Especies invasoras en España con información cartográfica %s en %s grupos" % (n_mdESPECIE, n_mdGRUPO))
print("Especies invasoras en España con información cartográfica en el mediterráneo español %s en %s grupos" % (n_bbESPECIE, n_bbGRUPO))

aaa=bbox[["GRUPO", "ESPECIE"]].drop_duplicates()
aaa.reset_index(drop=True, inplace=True)
aaa.to_excel("output/EspeciesUnicasMediterraneoEspaña.xlsx")