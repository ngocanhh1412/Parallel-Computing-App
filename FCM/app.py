from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import main
from fastapi.staticfiles import StaticFiles

import os
from dotenv import load_dotenv
load_dotenv()
PATH = os.getenv("OUTPUT_PATH")

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
    result = main(input_data.input_string)
    return {"result": result}

@app.get("/fcm_image")
async def img():
    # return FileResponse("D:\\DH\\Parallel Computing\\ProjectCuoiKy\\gray_py\\dl\\99_gray.png")
    output_path = os.path.join(PATH, "output_1.png")
    return FileResponse(f"{output_path}")
