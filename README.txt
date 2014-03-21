Framework “pyscrap3”

Mini framework orientado originalmente para web scraping, sirve para desarrollar y empaquetar
proyectos hechos en python3 separando en dos capas el manejo de la información
- en web scraping, la capa de extracción definida en una clase heredada de 'pyscrap3.Spider' y
la de capa de almacenamiento definida en pipeline.py-. 

Toda clase en el proyecto que herede de pyscrap3.Spider tendrá una función/generador 'parse()'
donde retornará una serie de Items o ListItems.

Cada Item o ListItem tendrá una función que se definirá
en pipeline.py con el objeto de procesar o almacenar dichos items.

El archivo donde se ubica la clase heredada de pyscrap3.Spider
no necesita pipeline.py obligatoriamente para funcionar. No existen
import explicitos de un archivo al otro para el desarrollador
de modo que ambas capas están, a la vista del programador, separadas.

Véase el proyecto de ejemplo instalando y ejecutando:

$ wscrap3

Instalación:

$ pip install pyscrap3

Nota: Por defecto los proyectos se crean con la licencia apache 2.0.