from fastapi import FastAPI,HTTPException
import json

app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data=json.load(f)

    return data

@app.get('/')
def home():
    return {'message':"you are exceuting the fast api file"}

@app.get('/health')
def health_check():
    return { 'status':'ok'}

@app.get('/details')
def patient_details():
    data=load_data()
    return data

@app.get('/patient_detail/{patient_id}')
def patient_Id_detail(patient_id):
    id=patient_id
    patient_id=f'P00{id}'
    data=load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(404,detail=f"{patient_id} Patient ID not found,enter the valid patient id")

data=load_data()
print(data.keys())