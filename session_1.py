from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def home():
    return {'message':"you are exceuting the fast api file"}

@app.get('/health')
def health_check():
    return { 'status':'ok'}
