# Mapping Marktstammdatenregister data to the Common Information Model (CIM) from IEC

> [!WARNING]
> This is Work in Progress
   

This repository transforms German energy data from the [Marktstammdatenregister (MaStR)](https://www.marktstammdatenregister.de/) into the [Common Information Model (CIM)](https://en.wikipedia.org/wiki/Common_Information_Model_(electricity)) standard from IEC TC57. In its first version, this repo only converts a small fraction of wind turbine attributes data into csv, but other generation types, attributes, and data formats could be also derived in future versions.

## What it does

1. **Data Extraction**: `main.py` queries a local SQLite database (downloaded via `open-mastr`) containing MaStR wind turbine data, including:
   - MaStR ID, wind park name, net rated power, manufacturer, type designation, and GPS coordinates

2. **Schema Mapping**: Uses [LinkML](https://linkml.github.io/linkml/) to transform MaStR data to CIM format:
   - `schema/mastr.yml` - Source schema generated from the MaStR SQLite DB using the linkml schema-automator and manually extended
   - `schema/map.yml` - Mapping rules defining how MaStR fields map to CIM attributes

3. **Metadata Generation**: `generate-metadata.sh` creates a CIM profile (`schema/cim-mastr-data-profile.yml`) from the base IEC CIM schema (`schema/im_tc57cim.yml`), including WindGeneratingUnit, maxOperatingP, aggregate, normallyInService, PositionPoint, and Length classes and writes the relevant information to the `metadata.json` file

## Output

The transformation produces `WindGeneratingUnits.csv` containing CIM-formatted wind generating unit data in csv format together with a json context metadata file.

## License
The original Marktstammdatenregister from Bundesnetzagentur für Elektrizität, Gas, Telekommunikation, Post und Eisenbahnen is licensed under [Datenlizenz Deutschland – Namensnennung – Version 2.0](https://www.govdata.de/dl-de/by-2-0).
