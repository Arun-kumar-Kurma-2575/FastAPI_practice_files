from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Literal,Optional

app=FastAPI()

class Patient(BaseModel):
    id: str=Field(...,description="ID of the patient")
    name: str=Field(...,description="Name of the Patient")
    city: str=Field(...,description="Patient belongs to which city")
    age: int=Field(...,description="Age of the Patient",gt=0)
    weight: float=Field(...,description='Weight of the Patient in Kgs',gt=0)
    height: float=Field(...,description='Height of the Patient in meters',gt=0)
    gender: Literal['male','female']=Field(...,description="gender of the patient")

    @computed_field
    @property
    def bmi(self)->float:
        bmi= (self.weight)/(self.height**2)
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
         

class Update_Patient(BaseModel):
    #id:Optional[str]=Field(...,description="Id of the patient")
    name:Optional[str]=Field(default=None,description="Name of the Patient")
    city:Optional[str]=Field(default=None,description="Patient belongs to which city")
    age:Optional[int]=Field(default=None,description="Age of the Patient")
    weight:Optional[float]=Field(default=None,description="Weight of the Patient")
    height:Optional[float]=Field(default=None,description="Height of the Patient in meters")
    gender:Optional[Literal['male','female']]=Field(default=None,description='Gender of the Patient')



def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)

    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)


@app.get('/')
def home():
    pass

@app.get('/health')
def health_check():
    pass

@app.get('/details')
def all_patient_details():
    data=load_data()
    return data

@app.get('/patient_detail/{patient_id}')
def individual_patient_details(patient_id):
    data=load_data()

    if patient_id  not in data:
        raise HTTPException(404,f"{patient_id} Patient_Id not found.Enter the valid PatientID ")
    else:
        return data[patient_id]
    

@app.post('/create')
def inserting_patient_detail(patient:Patient):
    data=load_data()
    if patient.id in data:
        raise HTTPException(402,f'{patient.id} patient id already exist')
    else:
        data[patient.id]=patient.model_dump(exclude='id')
    save_data(data)

    return JSONResponse(
        status_code=202,
        content={'message': f'{patient.id} inserted successfully'}
    )

@app.put('/edit/{patient_id}')
def updating_patient_details(patient_id:str,update_patient:Update_Patient):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(400,f"{patient_id} patient_id not valid. enter the valid patient id")
    
    existing_data=data[patient_id]
    new_data=update_patient.model_dump(exclude_unset=True)

    for key,value in new_data.items():
        existing_data[key]=value

    
    #############################################
    #existing_patient_info -> pydantic object -> updated bmi + verdict
    existing_data['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_data)
    #-> pydantic object -> dict
    existing_data = patient_pydantic_obj.model_dump(exclude='id')
    ################################

    data[patient_id]=existing_data
    save_data(data)

    return JSONResponse(status_code=200,content={'message':f'{patient_id}is updated'})
    