from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Literal

app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)

    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)

class Patient_detail(BaseModel):
    id : str=Field(...,description="Id of the patient",example="P001")
    name : str=Field(...,description="name of the patient")
    city : str=Field(...,description="city of the patient")
    age : int=Field(...,description="Age of the Patient")
    gender: Literal['male','female']=Field(...,description='Gender of the patient')
    height: float=Field(...,description='Height of the patient in the mtrs',gt=0)
    weight: float=Field(...,description="weight of the patient in kgs",gt=0)

    @computed_field
    @property
    def bmi(self)-> float:
        bmi=(self.weight/(self.height**2))
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18:
            return 'underweight'
        elif self.bmi<25:
            return 'Normal'
        elif self.bmi<30:
            return 'overweight'
        else :
            return "obese"
        





@app.get('/')
def home():
    return {'message':"you are exceuting the fast api file"}

@app.get('/health')
def health_check():
    return {'status':'ok'}

@app.get('/details')
def all_patient_details():
    data=load_data()

    return data

@app.get('/patient_details/{patient_id}')
def individual_patient_details(patient_id):
    patient_id=f'P00{patient_id}'
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(404,detail=f"{patient_id} not found, enter the valid patient id")

@app.post('/create')
def insert_patient_detail(patient_detail:Patient_detail):
    data=load_data()

    if patient_detail.id in data:
        raise HTTPException(404,f"{patient_detail.id} already exist")
    
    data[patient_detail.id]=patient_detail.model_dump(exclude='id')

    save_data(data)

    #return JSONResponse(202,{'message': f'{patient_detail.id} inserted successfully'})
    return JSONResponse(
        status_code=202,
        content={'message': f'{patient_detail.id} inserted successfully'}
    )





