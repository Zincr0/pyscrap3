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
from pyscrap3 import Spider
from items import DemoItem
from items import DemoListItems
#from IPython import embed


class webCrawler(Spider):

    def __init__(self):
        super().__init__()

    def parse(self, url, category=None):
        """Esta función/generador será llamada cuando se ejecute webCrawler().start() con
        los mismos parámetros.
        Cada Item o itemList tiene una función asociada en getPipes, en pipeline.py;
        dicha función será ejecutada al momento de retornar (yield) el item o
        itemList durante la ejecución de 'start()'."""
        print("url: '" + url + "' category: " + str(category))
        dItem = DemoItem()
        dItem["title"] = "some title"
        dItem["body"] = "a bunch of text"
        yield dItem
        lItems = DemoListItems()
        lItems["author"] = "Jhon Doe"
        lItems.append("comment 1")
        lItems.append("comment 2")
        yield lItems


a = webCrawler()

print("Loading urls from getUrls")
for url in a.getUrls():
    a.start(url)

print("Loading data from getSearchData")
for data in a.getSearchData():
    a.start(data["url"], data["category"])

