
from fastapi import FastAPI, Path, HTTPException, Query
import json

app  = FastAPI()

def load_data():
  with open('patients.json', 'r') as f:
    data  = json.load(f)
  return data

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