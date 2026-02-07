from fastapi import FastAPI,HTTPException
import json
from pydantic import BaseModel,Field

app=FastAPI()


# class Items(BaseModel):
#     item_name:str=Field(...,description="Names of the item")
#     item_rate:float =Field(...,description="Rate of the item")
class Cuisine(BaseModel):
    name: str=Field(...,description='Name of the cuisine')
    items: list[dict[str,float]]=Field(...,description="Names,rates of the items respectively")
    is_active: bool=Field(default=False,description="is the cuisine available")

class coupon(BaseModel):
    code: str=Field(...,description="Enter your Coupon code",example='SAVE10')
    discount:float=Field(default=0,description="Enter the discount based on the coupon code",lt=50)
    coupon_active:bool=Field(default=False,description="is the coupon code is active or not")

class Order(BaseModel):
    name:str=Field(...,description='Name of the cuisine')
    items:list[str]=Field(...,description="enter the item types")
    coupon_code:str=Field(...,description="enter the coupon code you have")


    

def load_data():
    with open('cuisines_1.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('cuisines_1.json','w') as f:
        json.dump(data,f)

def load_coupons():
    with open('coupons.json','r') as f:
        coupon_data=json.load(f)
    return coupon_data

def save_coupon(coupon_data):
    with open('coupons.json','w') as f:
        json.dump(coupon_data,f)




@app.get('/')
def home():
    return "welcome to the resturant webpage"

@app.get('/cuisines')
def get_cuisines():
    data=load_data()
    return data

@app.get('/cuisines/{name}')
def get_individual_cuisine(name:str):
    data=load_data()
    if name not in data:
        raise HTTPException(400,f'enter the valid cuisine names among {list(data.keys())}')

    l=data[name]
    return l


@app.post('/cuisines')
def inserting_new_cuisines(cuisine:Cuisine):
    data=load_data()
    if cuisine.name in data:
        raise HTTPException(400,f"enter the new cuisine {list(cuisine.name)} already exists")

    name=cuisine.name
    items=cuisine.items
    active=cuisine.is_active

    print(items)

    l=[]
    l.append(items)
    l.append(active)

    data[name]=l
    save_data(data)
    return data


@app.delete('/cuisine/{name}')
def deleting_cuisine(name):
    data=load_data()
    if name not in data:
        raise HTTPException(404,f"enter the valid cuisine name from {list(data.keys())} ")
    
    del(data[name])
    save_data(data)


@app.get('/coupons')
def get_coupons():
    coupon_data=load_coupons()
    return coupon_data


@app.get('/coupons/{name}')
def get_individual_coupons(name:str):
    coupon_data=load_coupons()
    return coupon_data[name]

@app.post('/coupons/{create}')
def insert_coupon(coupon:coupon):
    coupon_data=load_coupons()
    code=coupon.code
    discount=coupon.discount
    coupon_active=coupon.coupon_active
    l=[]
    l.append(discount)
    l.append(coupon_active)
    coupon_data[code]=l
    save_coupon(coupon_data)


@app.post('/orders')
def take_orders(order:Order):
    data=load_data()
    coupon_data=load_coupons()
    name=order.name
    items=order.items
    code=order.coupon_code
    c=0
    discount=0
    price=0
    if name in data:
        for i in items:
            c+=data[name][0][0][i]

    if code in coupon_data: # and coupon is active ==true
        discount=coupon_data[code][0]

    price=c*((100-discount)/100)
    return price




# data=load_data()
# print(type(data))