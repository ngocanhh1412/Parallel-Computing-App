from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import main
import uvicorn
from fastapi.staticfiles import StaticFiles

import os
from dotenv import load_dotenv
load_dotenv()
PATH2 = os.getenv("OUTPUT_PATH2")

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
    input_option: float

@app.post("/fcmParallel")
def add_endpoint(input_data: InputData):
    result = main(input_data.input_string, input_data.input_option)
    return {"result": result}

@app.get("/fcmParallel_image")
async def img():
    # return FileResponse("D:\\DH\\Parallel Computing\\ProjectCuoiKy\\gray_py\\dl\\99_gray.png")
    output_path = os.path.join(PATH2, "output_2.png")
    return FileResponse(f"{output_path}")
