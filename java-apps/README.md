# Java GUI Applications

This folder contains two simple Swing applications used for the university course "Methodologies for Application Development".

- **CitiesApp** – Reads `data/cities.txt` and displays a table with Greek and English names of selected cities.
- **NamedEntitiesApp** – Reads `data/namedEntities.txt` and displays a table with different named entities such as museums or airports.

Data files are encoded in UTF-8 and follow the format described in the assignment specification.

To run an application use:

```bash
javac CitiesApp/*.java
java -cp CitiesApp CitiesGUI
```

or

```bash
javac NamedEntitiesApp/*.java
java -cp NamedEntitiesApp NamedEntitiesGUI
```

The GUI simply lists the items and does not implement advanced features.
