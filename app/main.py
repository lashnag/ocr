import pytesseract
import base64
import logging
import re
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from io import BytesIO
from PIL import Image
from logger import init_logger

init_logger()
logging.getLogger().info("OCR run")
server = FastAPI()

class ImageRequest(BaseModel):
    base64Image: str

@server.post("/image-to-text")
def image_to_text(request: ImageRequest):
    try:
        image_data = base64.b64decode(request.base64Image)
        image = Image.open(BytesIO(image_data))
        rus_text = clean_text_russian(pytesseract.image_to_string(image, "rus"))
        eng_text = clean_text_english(pytesseract.image_to_string(image, "eng"))
        return JSONResponse(content={'ruText': rus_text, 'enText': eng_text})
    except Exception as error:
        logging.getLogger().error(f"Common error: {error}", exc_info=True)
        raise HTTPException(status_code=500, detail="Произошла ошибка при обработке изображения")

def clean_text_russian(text):
    text = re.sub(r'[^а-яА-ЯёЁ0-9\s,._!?«»–-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def clean_text_english(text):
    text = re.sub(r'[^a-zA-Z0-9\s,._!?\'\"()–-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()