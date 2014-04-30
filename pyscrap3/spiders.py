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
#from IPython import embed
import logging
import inspect
import importlib


def getEmptyPipes():
    """Estas 'pipes' vacías serán usadas en caso de que la función
    getPipes no este definida en pipeline.py"""
    pipes = {"items":
             {}, "itemLists": {}
             }
    return pipes


def emptyGetUrls(*args, **kwargs):
    logging.warning("getUrls not defined in pipeline.py")
    return None


def emptyGetSearchData(*args, **kwargs):
    logging.warning("getSearchData not defined in pipeline.py")
    return None


class Spider():
    """Esta clase enlaza las funcines getUrls y getSearchData
    definidas en pipeline.py a las funciones propias getUrls y getSearchData.
    Procesa todos los items que retorne la función 'parse' mediante la función 'start'."""
    def __init__(self):
        #embed()
        self.pipelineUrls = emptyGetUrls
        self.pipelineSearchData = emptyGetSearchData
        pipeline = None
        try:
            #try:
            #    print("1")
            #    from .pipeline import getUrls
            #    self.pipelineUrls = getUrls
            #except:
            try:
                #print("2")
                from pipeline import getUrls
                self.pipelineUrls = getUrls
            except ImportError as e:
                if e.msg == "No module named 'pipeline'" or e.msg == "cannot import name getUrls":
                    #print("3")
                    subpackage = inspect.getmodule(self.parse).__package__
                    try:
                        pipeline = importlib.import_module('.pipeline', subpackage)
                        self.pipelineUrls = pipeline.getUrls
                    except TypeError as e:
                        logging.warning("getUrls not defined in pipeline.py")
                else:
                    raise
        except ImportError as e:
            if e.msg == "No module named 'pipeline'" or e.msg == "cannot import name getUrls":
                logging.warning("getUrls not defined in pipeline.py")
            else:
                raise

        if pipeline:
            self.pipelineSearchData = pipeline.getSearchData
        else:
            try:
                #try:
                #    from .pipeline import getSearchData
                #    self.pipelineSearchData = getSearchData
                #except:
                from pipeline import getSearchData
                self.pipelineSearchData = getSearchData
            except ImportError as e:
                if e.msg == "cannot import name getSearchData":
                    logging.warning("getSearchData not defined in pipeline.py")
                else:
                    raise

    def start(self, *args, **kwargs):
        """Ejecuta la función/generador 'parse' y por cada
        Item o ItemList que retorne se ejecutará su función __parseItem__.
        Los objetos que no sean Item o Itemlist se ignorarán.
        Si se retorna un iterable, se intentará ejecutar la función __parseItem__
        de cada objeto que retorne dicho iterable."""
        for dataItem in self.parse(*args, **kwargs):
            try:
                #Si no existe se disparará el error
                dataItem.__parseItem__
            except AttributeError:
                #Puede que sea un iterable
                try:
                    for item in dataItem:
                        dataItem.__parseItem__()
                except:
                    pass
            try:
                dataItem.__parseItem__()
            except:
                pass

    def getUrls(self, *args, **kwargs):
        """Ejecuta la función/generador 'getUrls' que el usuario haya
        definido en pipeline.py"""
        yield from self.pipelineUrls(*args, **kwargs)

    def getSearchData(self, *args, **kwargs):
        """Ejecuta la función/generador 'getSearchData' que el usuario haya
        definido en pipeline.py"""
        yield from self.pipelineSearchData(*args, **kwargs)


class FieldNotDefined(Exception):
    """Esta excepción se disparará cuando se intente agregar
    un campo no definido, ejemplo: item['campoSinDefinir'] = 2"""
    def __init__(self, fieldName, itemName):
        self.fieldName = fieldName
        self.itemName = itemName

    def __unicode__(self):
        return "Field " + self.fieldName + \
               " not defined in item.py for item: " + self.itemName


class ItemList(list):
    """Unión de una lista y un diccionario. Se pueden añadir
    objetos de dos formas:
        1.- itemList["propiedad"] = objeto1
            Donde el campo "propiedad" debe ser especificado al crear la clase
            self.newfield("propiedad")
        2.- itemList.append(objeto2)
    Los objetos añadidos por cada método son independientes y nunca se mezclan.
    Para acceder:
        objeto1 = itemList["propiedad"]
        objeto2 = itemList[0]
    Al crear una clase heredada la función que esté definida en pipeline.py en
    getPipes se asociará con el nombre __parseItem__,
    ejemplo si:
    en pipeline.py:
        pipes = {"items":..."itemLists":{ "DemoListItems": saveListItems}}
    Al crear:
        demoList = DemoListItems()
    demoList tendrá la función 'saveListItems' asociada en demoList.__parseItem__"""
    def __init__(self):
        list.__init__(self)
        self.__fields__ = {}
        pipes = getEmptyPipes()
        self.__pipelineFunction__ = lambda *args, **kwargs: None

        try:
            try:
                from pipeline import getPipes
                pipes = getPipes()
            except:
                #print("3")
                subpackage = inspect.getmodule(self.parse).__package__
                pipeline = importlib.import_module('.pipeline', subpackage)
                pipes = pipeline.getPipes
        except:
            logging.warning("getPipes not defined in pipeline.py")

        className = self.__class__.__name__
        self.__pipelineFunction__ = pipes["itemLists"].get(className)
        #self.__funciones__

    def __parseItem__(self):
        """Llama la función asociada definida en pipeline.py"""
        self.__pipelineFunction__(self)

    def newfield(self, name, default=None):
        """Define un campo para ser manipulado en notación
        itemList["campoPorNombre"]"""
        self.__fields__[name] = default

    def getfields(self):
        return self.__fields__

    def __setitem__(self, keyField, value):
        """Agrega objetos, dependiendo de la notación
            itemList[<int>] = objeto1
        agregará un objeto a la lista interna.
            itemList[<objeto>] = objeto1
        agregará objeto1 al diccionario interno."""
        if type(keyField) == type(int()):
            list.__setitem__(self, keyField, value)
        else:
            if keyField in self.__fields__:
                self.__fields__[keyField] = value
            else:
                raise FieldNotDefined(keyField, self.__class__.__name__)

    def __getitem__(self, keyField):
        """Retorna objetos, dependiendo de la notación.
            itemList[<int>]
        retornará un objeto desde la lista interna.
            itemList[<objeto_key>]
        retornará un objeto desde el diccionario interno."""
        if type(keyField) == type(int()):
            return list.__getitem__(self, keyField)
        else:
            if keyField in self.__fields__:
                return self.__fields__.get(keyField)
            else:
                raise FieldNotDefined(keyField, self.__class__.__name__)


class Item():
    """Objeto estilo diccionario. Para añadir objetos:
        item["propiedad"] = objeto1
        El campo "propiedad" debe ser especificado al crear la clase
            self.newfield("propiedad")
        O se lanzará un excepción 'FieldNotDefined'.
    Para obtener objetos:
        objeto1 = item["propiedad"]
    Al crear una clase heredada la función que esté definida en pipeline.py en
    getPipes se asociará con el nombre __parseItem__,
    ejemplo si:
    en pipeline.py:
        pipes = {"items":{ "DemoItem": saveItem}...}
    Al crear:
        item = DemoItem()
    item tendrá la función 'saveItem' asociada en item.__parseItem__"""
    def __init__(self):
        self.__fields__ = {}
        pipes = getEmptyPipes()
        self.__pipelineFunction__ = lambda *args, **kwargs: None

        try:
            try:
                from pipeline import getPipes
                pipes = getPipes()
            except:
                #print("3")
                subpackage = inspect.getmodule(self.parse).__package__
                pipeline = importlib.import_module('.pipeline', subpackage)
                pipes = pipeline.getPipes
        except:
            logging.warning("getPipes not defined in pipeline.py")

        className = self.__class__.__name__
        self.__pipelineFunction__ = pipes["items"].get(className)
        #self.__funciones__

    def __parseItem__(self):
        """Llama la función asociada definida en pipeline.py"""
        self.__pipelineFunction__(self)

    def newfield(self, name, default=None):
        """Define un campo para ser manipulado en notación
        itemList["campoPorNombre"]"""
        self.__fields__[name] = default

    def get(self, keyField):
        return self.__fields__.get(keyField)

    def getDict(self):
        return self.__fields__

    def __getitem__(self, keyField):
        if keyField in self.__fields__:
            return self.__fields__.get(keyField)
        else:
            raise FieldNotDefined(keyField, self.__class__.__name__)

    def __setitem__(self, keyField, value):
        if keyField in self.__fields__:
            self.__fields__[keyField] = value
        else:
            #print("field '"+keyField+"' not defined!, ignoring.")
            raise FieldNotDefined(keyField, self.__class__.__name__)
