import pandas as pd
import geopandas as gpd

def download_gis(gis_url):
    map_data = gpd.GeoDataFrame()
    try:
        map_data=gpd.read_file(url)
    except:
        print("ERROR DOWNLOADING")
        pass
    return map_data


df = pd.read_excel("downloads/speciesRAW.xlsx", index_col=0)
df = df.fillna('')  

md1 = gpd.GeoDataFrame(columns=['CUADRICULA', 'MARINO', 'Catalogo', 'Reglamento', 'EASIN', 'EIDOS', 'N', 'geometry'])

for index,row in df.iterrows():
    print(index)
    url=row.GIS
    if url!="":
        try:
            md = download_gis(url)
            try:

                    md.rename(columns={"N":"ESPECIE"},inplace=True)
                    md["ESPECIE"] = row.NOMBRE
                    md["GRUPO"] = row.GRUPO
                    md1=md1.append(md, ignore_index=True)

            except:
                print("Assignation ERROR")
                pass
        except:
            pass



mdd=md1[["GRUPO","ESPECIE","geometry"]]
mdd = mdd.set_crs('epsg:25830')
mdd.to_file('output/md.shp', driver='ESRI Shapefile')
