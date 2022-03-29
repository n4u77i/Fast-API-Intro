from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str]


class UpdateItem(BaseModel):
    name: Optional[str]
    price: Optional[float]
    brand: Optional[str]
    
    
inventory = {}

@app.get('/get-item/{item_id}')
def get_items(item_id: int = Path(None, description='The id of the item you want to view', gt=0)):
    if item_id in inventory:
        return inventory[item_id]
    raise HTTPException(404, "Item ID not found")


# By default, python won't allow to write required params after optional params (order is restricted).
# '*' in the first parameter of a function tells python to write parameters in any order.
@app.get('/get-by-name')
def get_items(*, name: Optional[str] = Query(..., description='Required name query parameter')):
    for item_id in inventory:
        print(item_id)
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(404, "Item name not found")


@app.post('/create-item/{item_id}')
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(400, "Item ID already exists")
    
    # inventory[item_id] = {
    #     'name': item.name,
    #     'price': item.price,
    #     'brand': item.brand
    # }
    inventory[item_id] = item
    
    return inventory[item_id]


@app.put('/create-item/{item_id}')
def create_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(404, "Item with ID does not exist")
    
    if item.name != None:
        inventory[item_id].name = item.name
        
    if item.price != None:
        inventory[item_id].price = item.price
        
    if item.brand != None:
        inventory[item_id].brand = item.brand
    
    return inventory[item_id]


@app.delete('/delete-item')
def delete_item(item_id: int = Query(..., description='The ID of the item you want to delete')):
    if item_id not in inventory:
        raise HTTPException(404, "Item with ID does not exist")
    
    del inventory[item_id]
    return {"Success": "Item deleted!"}