from typing import Optional, Set
from enum import Enum
from fastapi import FastAPI, Header
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    '''
        Esse é o esquema que está sendo aguardado no post de items..
        Possui argumentos opcionais e obrigatorios
    '''
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []
    image: Optional[Image] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "The pretender",
                "price": 42.0,
                "tax": 3.2,
                "tags": ["rock", "metal", "bar"],
                "image": {
                    "url": "http://example.com/baz.jpg",
                    "name": "The Foo live"
                }
            }
        }


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Usando para o exemplo
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
# Utilizar os query parameter skip e limit : ...?skip=1&limit=10
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10, q: Optional[str] = None):
    if q:
        return {'Q': q}
    return fake_items_db[skip : skip + limit]

@app.get("/items/{item_id}")
def read_item(
        item_id: int,
        strange_header: Optional[str] = Header(None, convert_underscores=True)    
    ):
    try:
        return {"item_id": fake_items_db[item_id], "header": strange_header}
    except:
        return {"error": f"Não localizada a posição {item_id}"}

# Testando Post: O Argumento para a função se baseia na Classe BaseModel criada para 'parsear''
# o Json que se recebe no post e fazer o que é necessário...
@app.post("/items/")
async def create_item(item: Item):
    fake_items_db.append(item)
    return item


@app.get("/partners")
async def read_partner(q: Optional[str] = None):
    return [
        {"name": "Diogo", "doc": "351058588543"},
        {"name": "ligia".title(), "doc": "351058533444"},
        {"name": "Eduardo", "doc": "351052323233"},
        {"name": "Anastacia", "doc": "676666568571"},
        {"name": "Mel", "doc": "851778588473"},
    ]

# Baseado no enum declarado na Classe ModelName, aceita apenas argumentos de uma lista fixa...
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}
    # Caso não for nenhum dos itens do enum, retorna um Erro...