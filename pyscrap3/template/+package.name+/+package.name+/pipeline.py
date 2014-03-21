#Copyright 2014 Daniel Osvaldo Mondaca Seguel
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.


def getPipes():
    """Asocia una función con un item o un ListItem respectivo.
    Al momento en que la función 'parse' retorne un item o ItemList,
    dicha función ejecutará."""
    pipes = {"items":
             {
             "DemoItem": saveItem
             },
             "itemLists":
             {
             "DemoListItems": saveListItems
             }
             }
    return pipes


def getUrls():
    """Generador, acá se pueden obtener las url a procesar desde la base de datos"""
    yield "http://www.some_news_site.cl"
    yield "http://www.another_news_site.cl"


def getSearchData():
    """Generador, acá se puede obtener la data a procesar desde la base de datos"""
    yield {"url": "http://www.some_cats_site.cl", "category": "cats"}
    yield {"url": "http://www.some_dogs_site.cl", "category": "dogs"}


def saveItem(item):
    print("saving item " + str(item))


def saveListItems(items):
    print("Saving list items")
    for item in items:
        print(item)


