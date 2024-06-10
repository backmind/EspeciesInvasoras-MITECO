# import urllib.request
import requests
import io
import PyPDF2
import re
import pandas as pd
df = pd.read_excel("downloads/speciesRAW.xlsx", index_col=0)
df = df.fillna('')  

# Open a PDF file.
secciones="Nombre vulgar;Posición taxonómica;Observaciones taxonómicas;Resumen de su situación;Normativa nacional;Normativa autonómica;Normativa europea;Acuerdos y Convenios internacionales;Listas y Atlas de Especies Exóticas Invasoras;Área de distribución;Vías de entrada y;Descripción del hábitat y;Impactos y amenazas;Medidas y nivel de dificultad para su control;Bibliografía;Fecha de modificación de la Memoria:".replace("especie","Especie")
delim=secciones.split(";")
columnas=secciones.replace(" ", "_").lower().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u").upper().replace(":","").split(";")[:-1]
columnas[10]="VIAS_DE_ENTRADA"
columnas[11]="DESCRIPCION_DEL_HABITAT"
columnas.append("DATE")
def find_between(s, start, end):
    try:
        text=(s.split(start))[1].split(end)[0]
    except:
        text=""
        print("Error with %s in %s" %(url, start))
    return text

def parse_pdf(pdf_url, SAVE_PDF = False):
    r = requests.get(pdf_url)
    # file = urllib.request.urlopen(pdf_url)
    fp=io.BytesIO(r.content)
    pdfReader = PyPDF2.PdfFileReader(fp)
    parsed_text=""
    for i in range(pdfReader.numPages):
        pageObj = pdfReader.getPage(i)
        parsed_text+=pageObj.extractText().encode('utf-8', 'ignore').decode("utf-8")
    # parsed_text =parsed_text.strip().replace("\n","").replace("\s+"," ").replace("ﬂ","\"").replace("especie","Especie")
    parsed_text = re.sub("\n|\t|\s{2,}", " ", parsed_text).strip().replace("ﬂ","\"").replace("especie","Especie").replace("al .", "al.").replace("Fami lia","Familia").replace("Cat álogos", "Catálogos")
    parsed_text = re.sub(" Página \d+ de \d+","",parsed_text)
    parsed_text = parsed_text.replace("Resumen de su situación e impacto en España","Resumen de su situación").replace("Resumen de su situación e impacto en España","Resumen de su situación").replace("Resumen de su posible situación e impacto en España","Resumen de su situación").replace("Resumen de su situación e impacto en España","Resumen de su situación").replace("Resumen de su situación e impacto en España","Resumen de su situación")
    parsed_text = parsed_text.replace("Acuerdos y Convenios Internacionales","Acuerdos y Convenios internacionales")
    parsed_text = parsed_text.replace("Descripción del hábitat y bilogía de la especie","Descripción del hábitat y biología de la Especie").replace("Descripción del hábitat y bilogía de la especie","Descripción del hábitat y biología de la Especie")
    parsed_text = parsed_text.replace("Medidas para su control","Medidas y nivel de dificultad para su control")
    if SAVE_PDF:
        fn = pdf_url.split("/")[-1]
        with open(f"downloads/pdf/{fn}", "wb") as f:
            f.write(r.content)
    return parsed_text

def extract_data(keys, delim, parsed_text):
    data={}
    for i in range(len(delim)):
        if i == len(delim)-1:
            data[keys[i]] = parsed_text.split(":")[-1].strip()
        else:
            try:
                data[keys[i]]=find_between(parsed_text,delim[i],delim[i+1]).strip()
            except:
                pass
    return data

df_data = pd.DataFrame(columns=columnas)
for index,row in df.iterrows():
    print(index)
    url=row.PDF
    if url!="":
        parsed_text=parse_pdf(url, SAVE_PDF=True)
        dt=extract_data(columnas, delim, parsed_text)
        try:
            if dt!={}:
                df_data.loc[index]=dt
            else:
                print("Error with "+url)
        except:
            print("Mismatched with "+url)
    else:
        print("%s has no pdf"%(row.NOMBRE))
    

df_complete=pd.merge(df, df_data, left_index=True, right_index=True, how="outer")

# Limpiando un poco la data
df_complete["RESUMEN_DE_SU_SITUACION"] = df_complete.RESUMEN_DE_SU_SITUACION.str.replace("en España como Especie exótica ","").str.replace("en España como Especie exótica","")
df_complete["AREA_DE_DISTRIBUCION"] = df_complete.RESUMEN_DE_SU_SITUACION.str.replace("y evolución de la población ","").str.replace("y evolución de la población","")
df_complete["VIAS_DE_ENTRADA"] = df_complete.RESUMEN_DE_SU_SITUACION.str.replace("^expansión ","").str.replace("^expansión - ","")
df_complete["DESCRIPCION_DEL_HABITAT"] = df_complete.RESUMEN_DE_SU_SITUACION.str.replace("^biología de la Especie ","").str.replace("^biología de la Especie - ","").str.replace("^biología de la espec ie ","").str.replace("^biología de las Especies ","")
df_complete["NORMATIVA_NACIONAL"] = df_complete.RESUMEN_DE_SU_SITUACION.str.replace("Incluid a","Incluida").str.replace("incluid a","incluida").str.replace("i ncluido","incluido")
df_complete["NORMATIVA_AUTONOMICA"] = df_complete.RESUMEN_DE_SU_SITUACION.str.replace("Incluid a","Incluida").str.replace("incluid a","incluida").str.replace("i ncluido","incluido")
df_complete["NORMATIVA_EUROPEA"] = df_complete.RESUMEN_DE_SU_SITUACION.str.replace("Incluid a","Incluida").str.replace("incluid a","incluida").str.replace("i ncluido","incluido")

# Guardando
df_complete.to_excel("output/pdf_procesados.xlsx")

 