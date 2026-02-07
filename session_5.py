# from fastapi import FastAPI
# from enum import Enum

# app = FastAPI()
# @app.get('/')
# def home():
#     return "hello"

# @app.get("/hello")
# async def hello():
#     return "Welcome"

# @app.get("/hello/{name}")
# async def hello(name):
#     return f"Welcome {name}"

# class AvailableCuisines(str, Enum):
#     indian = "indian"
#     american = "american"
#     italian = "italian"
    
# food_items = {
#     'indian' : [ "Samosa", "Dosa" ],
#     'american' : [ "Hot Dog", "Apple Pie"],
#     'italian' : [ "Ravioli", "Pizza"]
# }

# @app.get("/get_items/{cuisine}")
# async def get_items(cuisine: AvailableCuisines):
#     return food_items.get(cuisine)


# coupon_code = {
#     1: '10%',
#     2: '20%',
#     3: '30%'
# }

# @app.get("/get_coupon/{code}")
# async def get_items(code: int):
#     return { 'discount_amount': coupon_code.get(code) }

from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from typing import Literal,Optional

app = FastAPI()
food_items = {
    'indian' : [ "Samosa", "Dosa" ],
    'american' : [ "Hot Dog", "Apple Pie"],
    'italian' : [ "Ravioli", "Pizza"]
}
coupon_code = {
    1: '10%',
    2: '20%',
    3: '30%'
}
cusine_types=food_items.keys()
cupon_types=coupon_code.keys()

class cusine(BaseModel):
    type:str=Field(...,description='enter the cusine type')
    types:list[str]=Field(default=[],description='enter the types of vaieties available')
#     type: =Field(...,description='enter the cusine type')
#     #discount: Literal[1,2,3]=Field(...,description="enter the type of discount")


class cusine_update(BaseModel):
    type:str=Field(...,description='enter the cusine type')
    types:Optional[list[str]]=Field(default=None,description='enter the types of vaieties available')





@app.get('/')
def home():
    return "hello"

@app.get('/all_items')
def get_all_items():
    return food_items 

@app.get('/get_items')
def get_items(cusine_type:Literal['indian','american','italian']):
    print(cusine_type)
    return food_items[cusine_type]

@app.get('/get_discount')
def get_discount(cusine_discount:Literal[1,2,3]):
    cusine_discount=int(cusine_discount)
    return coupon_code[cusine_discount]

@app.get('/get_items/{cusine_type}')
def get_items(cusine_type:str):
    print(cusine_type)
    if cusine_type not in food_items:
        raise HTTPException(404,f"cusine type not found select from the {food_items.keys()} only")
    else:
        return food_items[cusine_type]

@app.get('/get_discount/{discount}')
def get_discount(discount:int):
    return coupon_code[discount]

@app.post('/new_cusine')
def adding_new_cusine(cusine:cusine)-> dict:
    cusine_type=cusine.type
    cusine_types=cusine.types
    print(cusine_type)
    print(cusine_types)

    food_items[cusine_type]=cusine_types
    return food_items

@app.put('/update_cusine')
def updating_the_cusine(cusine_update:cusine_update):
    if cusine_update.type not in food_items:
        raise HTTPException(400,f'Enter the correct cusine type from {list(food_items.keys())}')
    else:
        type=cusine_update.type
        existing_cusine=food_items[type]
        new_cusine=cusine_update.types
        l=existing_cusine + new_cusine
        overall_cusines=set(l)
        food_items[type]=list(overall_cusines)
        return food_items












