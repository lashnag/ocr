import pytesseract
import base64
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from io import BytesIO
from PIL import Image

logging.getLogger().info("OCR run")
server = FastAPI()

class ImageRequest(BaseModel):
    base64Image: str

@server.post("/image-to-text")
def image_to_text(request: ImageRequest):
    image_data = base64.b64decode(request.base64Image)
    image = Image.open(BytesIO(image_data))
    text = pytesseract.image_to_string(image)
    return JSONResponse(content={'text': text})