# EspeciesInvasoras-MITECO

[![License: CC0-1.0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](http://creativecommons.org/publicdomain/zero/1.0/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

ETL pipeline to download, parse, and spatially process the **Spanish Catalogue of Invasive Alien Species** (Catálogo Español de Especies Exóticas Invasoras) published by the Spanish Ministry for Ecological Transition (MITECO).

## Description

The catalogue is regulated under [Real Decreto 630/2013](https://www.boe.es/buscar/act.php?id=BOE-A-2013-7722) and lists alien species whose introduction or release into the wild is prohibited in Spain. For each species, MITECO publishes a technical PDF fact sheet and, where available, a GIS layer with spatial distribution data.

This project automates the full acquisition and processing workflow in three stages:

1. **Web scraping** — `species_fetcher.py` crawls the MITECO catalogue page and builds a master index of all species with their associated resource URLs.
2. **PDF ETL** — `pdf_processer.py` downloads every technical fact sheet, extracts structured data from the PDFs, and consolidates the results into a single Excel file.
3. **GIS merge** — `gis_processer.py` downloads all per-species spatial layers and merges them into a unified shapefile.

> **Note on data availability:** All output artefacts (downloaded PDFs, processed Excel files, and GIS layers) are included directly in this repository. The original MITECO endpoints may change or become unavailable over time; having the data in the repository ensures long-term reproducibility.

## Academic citation

Data produced by this pipeline contributed to the following peer-reviewed study:

> Martínez-Megías, C., Rico, A. et al. (2022). *Biodiversity impacts by multiple anthropogenic stressors in Mediterranean coastal wetlands.* **Science of the Total Environment**, 818, 151712.
> https://doi.org/10.1016/j.scitotenv.2021.151712

Specifically, `output/EspeciesUnicasMediterraneoEspaña.xlsx` — the list of invasive species recorded in the Spanish Mediterranean coast — was used in the stressor analysis of that study.

## Data sources

| Source | URL | Format |
|--------|-----|--------|
| MITECO species catalogue (web) | https://www.miteco.gob.es/es/biodiversidad/temas/conservacion-de-especies/especies-exoticas-invasoras/ce-eei-catalogo.aspx | HTML |
| MITECO technical fact sheets | One PDF per species (URLs in `downloads/speciesRAW.xlsx`) | PDF |
| MITECO GIS distribution layers | One ZIP/SHP per species (URLs in `downloads/speciesRAW.xlsx`) | Shapefile |
| Mediterranean study area | Included in `input/` | Shapefile |

## Project structure

```
EspeciesInvasoras-MITECO/
├── species_fetcher.py          # Stage 1 — scrape catalogue & build species index
├── pdf_processer.py            # Stage 2 — download & parse PDF fact sheets
├── gis_processer.py            # Stage 3 — download & merge GIS layers
├── procesar_mediterraneo.py    # Example — filter species by spatial intersection
├── requirements.txt
├── input/
│   └── mediterranean_invspp.*  # Input shapefile: Spanish Mediterranean study area
├── downloads/
│   ├── speciesRAW.xlsx         # Master species index with resource URLs (13 KB)
│   └── pdf/                    # ~90 official MITECO technical fact sheets (~15 MB)
└── output/
    ├── pdf_procesados.xlsx              # Structured data extracted from PDFs (243 KB)
    ├── md.shp / md.dbf / md.shx / ...  # Unified invasive species GIS layer (~14 MB, EPSG:25830)
    └── EspeciesUnicasMediterraneoEspaña.xlsx  # Species intersecting the Mediterranean area (7.7 KB)
```

## Prerequisites

- **Python 3.9**
- **GDAL** (required by GeoPandas). On Windows, the easiest installation path is via conda:
  ```
  conda install -c conda-forge geopandas
  ```
  On Linux/macOS, `pip install geopandas` typically handles GDAL automatically.

## Installation

```bash
git clone https://github.com/<your-username>/EspeciesInvasoras-MITECO.git
cd EspeciesInvasoras-MITECO
pip install -r requirements.txt
```

## Usage — Full pipeline

All four scripts are run from the project root. If you only need the pre-built output data, you can skip directly to the example step.

### Stage 1 — Scrape species catalogue

```bash
python species_fetcher.py
```

Crawls the MITECO website and writes `downloads/speciesRAW.xlsx` with one row per species containing its name, taxonomy, and URLs for the PDF and GIS resources. Estimated runtime: ~2–5 min (network-bound).

### Stage 2 — Download and parse PDF fact sheets

```bash
python pdf_processer.py
```

Downloads ~90 PDFs into `downloads/pdf/` and extracts structured fields from each one. Output: `output/pdf_procesados.xlsx`. Estimated runtime: ~5–15 min (network + PDF parsing).

### Stage 3 — Download and merge GIS layers

```bash
python gis_processer.py
```

Downloads per-species GIS layers and merges them into a single shapefile `output/md.shp` (CRS: EPSG:25830, Spanish national grid). Estimated runtime: ~10–30 min (network-bound).

### Example — Filter by Mediterranean study area

```bash
python procesar_mediterraneo.py
```

Performs a spatial intersection between `output/md.shp` and the Mediterranean study area in `input/mediterranean_invspp.shp`. Output: `output/EspeciesUnicasMediterraneoEspaña.xlsx`, a list of unique invasive species present in that region.

## Output data description

### `downloads/speciesRAW.xlsx`

| Column | Description |
|--------|-------------|
| `especie` | Scientific species name |
| `grupo` | Taxonomic group (e.g., Aves, Plantas, Peces) |
| `url_pdf` | URL to the MITECO technical PDF fact sheet |
| `url_gis` | URL to the MITECO GIS distribution layer |

### `output/pdf_procesados.xlsx`

One row per species. Contains all fields extracted from the PDF fact sheets, including taxonomy, legal status, ecological impact descriptors, and management notes.

### `output/md.shp` (GIS layer)

Unified shapefile merging all per-species distribution layers.

| Field | Description |
|-------|-------------|
| `GRUPO` | Taxonomic group |
| `ESPECIE` | Scientific species name |
| `geometry` | Species distribution polygon/multipolygon |

CRS: **EPSG:25830** (ETRS89 / UTM zone 30N — Spanish national grid).

### `output/EspeciesUnicasMediterraneoEspaña.xlsx`

List of invasive alien species whose distribution intersects the Spanish Mediterranean coastal study area. Used as input data in Martínez-Megías et al. (2022).

## Compatibility note

This project was developed in 2020 and verified against the library versions listed in `requirements.txt`. If you use newer versions, note the following known breaking changes:

- **pandas ≥ 2.0**: `GeoDataFrame.append()` was removed → replace with `pd.concat()`.
- **PyPDF2 ≥ 3.0**: `PdfFileReader` was removed → replace with `PdfReader`.

## License

[CC0 1.0 Universal](LICENSE) — This work has been dedicated to the public domain. You may copy, modify, distribute, and perform the work, even for commercial purposes, without asking permission.
