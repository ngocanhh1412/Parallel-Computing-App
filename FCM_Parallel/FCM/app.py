from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import main
import subprocess
import os

from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Thêm middleware để cho phép truy cập từ tên miền khác
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    input_string: str

@app.post("/fcm")
def add_endpoint(input_data: InputData):
    result = main(input_data.input_string,option = 2)
    return {"result": result}

@app.post("/fcm_parallel")
def add_endpoint(input_data: InputData):
    result = main(input_data.input_string, option = 1)
    return {"result": result}