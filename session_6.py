from fastapi import FastAPI,HTTPException
import json
from pydantic import BaseModel,Field

# with open('cuisines.json','r') as f:
#     data=json.load(f)


# new_data=[["Hot Dog", "Apple Pie"],"True"]

# data['american']=new_data

# print(data)

# with open('cuisines.json','w') as f:
#     json.dump(data,f)


#########################################
app=FastAPI()

class Cuisine(BaseModel):
    name: str=Field(...,description='Name of the cuisine')
    items: list[str]=Field(...,description="Names of the items")
    is_active: bool=Field(default=False,description="is the cuisine available")

def load_data():
    with open('cuisines.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('cuisines.json','w') as f: 
        json.dump(data,f)




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



# data=load_data()
# print(type(data))

########################################

