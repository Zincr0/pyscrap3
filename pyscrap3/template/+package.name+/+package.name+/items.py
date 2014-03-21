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
from pyscrap3 import Item
from pyscrap3 import ItemList


class DemoItem(Item):
    """Los Item son ideales para guardar contenido único como el
    título de una página o el cuerpo de una noticia."""
    def __init__(self):
        super().__init__()
        self.newfield("title")
        self.newfield("body")


class DemoListItems(ItemList):
    """Las ItemList son ideales para guardar multiples contenidos
    agrupados, como todos los comentarios de un solo autor."""
    def __init__(self):
        super().__init__()
        self.newfield("author")
