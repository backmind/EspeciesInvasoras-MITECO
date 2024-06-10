# EspeciesInvasoras-MITECO
Este es un ejemplo sencillo que hace tres cosas:

- Webscraping
- PDFparsing
- GIS parsing y procesado

## Inicio
En la web del Ministerio para la Transición Ecológica y el Reto Demográfico se encuentra un catálogo de [especies invasoras de España](https://www.miteco.gob.es/es/biodiversidad/temas/conservacion-de-especies/especies-exoticas-invasoras/ce-eei-catalogo.aspx). Cada una de estas especies puede tener un pdf asociado y una capa GIS con información espacial de dónde se encuentra esta especie.

Lo que se pretende con este ejercicio es listar todas las especies invasoras de España y, para cada una, descargar su pdf técnico y su capa GIS asociada. Los pdf serán interpretados y procesados para obtener un excel destilado con toda la información. Las capas espaciales una vez descargadas serán procesadas e integradas en una capa única con todas estas especies invasoras.

Por último, se dejará un pequeño ejercicio resuelto para seleccionar solo las especies invasoras correspondientes al levante español, mediante procesado espacial.

### Obtener todas las especies
Lo primero que debemos hacer es correr el código `species_fetcher.py`, que recorrerá la web del ministerio obteniendo todos los enlaces de cada una de las especies. La salida de este código se encontrará en `downloads\speciesRAW.xlsx`. Los demás códigos usarán este archivo excel

### Obtener y procesar todos los pdf
A continuación, podremos ejecutar el código `pdf_processer.py`, el cual irá cargado y recorriendo cada uno de los enlaces para cada especie, descargando su pdf técnico. Luego hará ETL sobre todos estos archivos (que pueden ser guardados automáticamente en `downloads\pdf\`) dando como resultado el archivo excel `output\pdf_procesados.xlsx`

### Obtener y procesar todas las capas gis
Lo siguiente será hacer lo propio con las capas gis, de información espacial, para cada una de las especies invasoras. Para ello correremos el código `gis_processer.py`. Este código integrará todas las capas de las especies invasoras en una sola, y la guardará como `output\md.shp`

### Filtrar las especies invasoras espacialmente
Por último, para buscar las especies invasoras encontradas en una zona geográfica concreta de nuestro país, lo que se hará será cargar una capa objetivo (como ejemplo he dejado una capa que comprende el levante español, se encuentra en `input\mediterranean_invspp.shp`) y cruzarla con la información obtenida en el punto anterior. Se listan las especies que intersecan entre esta capa y la del punto anterior. La salida de este ejemplo se puede consultar en el excel `output\EspeciesUnicasMediterraneoEspaña.xlsx`

## Dependencias

Este ejercicio ha sido hecho mediante Python 3.9. 

Puedes ver las dependencias en el archivo *requirements.txt*. Puedes instalar estos requerimientos a través de la línea `pip install -r /path/to/requirements.txt`

> beautifulsoup4==4.12.3
> 
> geopandas==0.10.2
> 
> pandas==2.0.3
> 
> PyPDF2==3.0.1
> 
> Requests==2.32.3

