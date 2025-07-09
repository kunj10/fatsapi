
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse

import json
from pydantic import BaseModel, computed_field
from typing import List, Dict, Annotated , Optional 
app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Path(description="The ID of the patient to view")]
    name: Annotated[str, Path(description="The name of the patient")]
    city: Annotated[str, Path(description="The city of the patient")] 
    age: int
    gender: str
    height: float
    weight: float
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)
      
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif 18.5 <= self.bmi < 24.9:
            return "Normal weight"
        elif 25 <= self.bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"
class PatientUpdate(BaseModel):
    id: Annotated[Optional[str], Path(description="The ID of the patient to view")]
    name: Annotated[Optional[str], Path(description="The name of the patient")]
    city: Annotated[Optional[str], Path(description="The city of the patient")] 
    age: Optional[int] 
    gender: Optional[str]
    height: Optional[float]
    weight: Optional[float]

def load_data():
  with open('patients.json', 'r') as f:
    data  = json.load(f)
  return data

def save_data(data):
  with open('patients.json', 'w') as f:
    json.dump(data, f)

@app.get("/")
def  hello():
  return {'message' : 'Patient Management System API'}

@app.get("/about")
def  about():
  return {'message' : 'This is a Patient Management System API built with FastAPI.'}

@app.get("/view")
def view():
  data = load_data()
  return {'patients': data}

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient to view")): 
  patient_id = patient_id.upper()
  data = load_data()
  if patient_id in data:
      return {'patient': data[patient_id]}
  raise HTTPException(status_code = 404, detail = "Patient not Found")

#quey parameters
@app.get("/sort")
def sort(
    sort_by: str = Query(..., description="Field to sort by"),
    order: str = Query('asc', description="Field to sort by")
):
  valid_sort_fields = ['name', 'age', 'bmi' , 'height']
  valid_sort_orders = ['asc', 'desc']  
  if sort_by not in valid_sort_fields:
      raise HTTPException(status_code=400, detail="Invalid sort field. Enter from 'name', 'age', 'bmi'")
  if order not in valid_sort_orders:
      raise HTTPException(status_code=400, detail="Invalid sort field. Enter from 'asc', 'desc'")
  data = load_data()
  sorted_data = sorted(data.items(), key=lambda x: x[1][sort_by], reverse=(order == 'desc'))
  return sorted_data


@app.post('/create')
def create_patient(patient: Patient):

    # load existing data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})

@app.put('/update/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
  data = load_data()
  patient_id = patient_id.upper()
  if patient_id not in data:
      raise HTTPException(status_code=404, detail='Patient not found')
  # update the patient data
  existing_patient_info = data[patient_id]
  updated_patient_info = patient_update.model_dump(exclude_unset=True)
  
  for key, value in updated_patient_info.items():
    existing_patient_info[key] = value
  
  existing_patient_info['id'] = patient_id  # ensure the ID remains the same  
  # create a new Patient instance with the updated info
  patient_pydantic = Patient(**existing_patient_info)
  existing_patient_info  = patient_pydantic.model_dump(exclude='id')  
  
  data[patient_id] = existing_patient_info  
  save_data(data)
  return JSONResponse(status_code=200, content={'message': 'Patient updated successfully'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
  data = load_data()
  patient_id = patient_id.upper()
  if patient_id not in data:
      raise HTTPException(status_code=404, detail='Patient not found')
  
  del data[patient_id]
  save_data(data)
  
  return JSONResponse(status_code=200, content={'message': 'Patient deleted successfully'})