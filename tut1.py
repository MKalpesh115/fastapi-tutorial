from fastapi import FastAPI, Path, HTTPException, Query
import json
app= FastAPI()

def data_load():
    with open('pat.json', 'r') as f:
        data = json.load(f)
    return data

@app.get('/')
def hello():
    return {'message':'hello world'}

@app.get('/about')
def about():
    return {'message':' i am kalpesh'}

@app.get('/view')
def view():
    data=data_load()
    return data


@app.get('/pat/{patient_id}')
def view_pat(patient_id : str = Path(..., description='Id of patient in the DB', example='P001')):
    data =data_load()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='patient not found')


@app.get('/sort')
def sort_patients(sort_by:str=Query(..., description='Sort on the basis of height, weight or bmi'), order: str=Query('asc', description='hdbw')):
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail='invalid field {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='invalid field')
    
    data= data_load()

    sorted_data= sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=True)

    return sorted_data