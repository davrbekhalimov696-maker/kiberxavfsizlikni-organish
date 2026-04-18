import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from pydantic import BaseModel
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

app = FastAPI(title="CyberZone Pro Platform")

# Statik yo'llarni belgilash
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")

# CSS, JS va Rasmlar uchun statik ulanish
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# HTML shablonlari uchun Jinja2
templates = Jinja2Templates(directory=static_dir)

# Gemini AI sozlamalari
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class ChatRequest(BaseModel):
    message: str
    lang: str = "uz"
    module: str = "general"

# O'quv kontenti (Buni kengaytirishingiz mumkin)
CYBER_CONTENT = {
    "kirish": {
        "uz": {
            "title": "Kiberxavfsizlik asoslari",
            "theory": "Kiberxavfsizlik — bu raqamli aktivlarni himoya qilish.",
            "video": "https://www.youtube.com/embed/z5nc9MDbvEk"
        },
        "en": {
            "title": "Cybersecurity Fundamentals",
            "theory": "Cybersecurity is the protection of digital assets.",
            "video": "https://www.youtube.com/embed/inWWhr5tnEA"
        }
    },
    "kripto": {
        "uz": {
            "title": "Kriptografiya",
            "theory": "Ma'lumotlarni shifrlash va himoyalash usullari.",
            "video": "https://www.youtube.com/embed/8v6L0X-p_u4"
        },
        "en": {
            "title": "Cryptography",
            "theory": "Methods of encrypting and securing data.",
            "video": "https://www.youtube.com/embed/NuyzuNBFWbc"
        }
    }
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/module/{name}")
async def get_module(name: str, lang: str = "uz"):
    module = CYBER_CONTENT.get(name, {}).get(lang)
    if not module:
        raise HTTPException(status_code=404, detail="Modul topilmadi")
    return module

@app.post("/ask")
async def ask_ai(request: ChatRequest):
    try:
        instruction = f"Sen kiberxavfsizlik mentorsan. Javob tili: {request.lang}. Mavzu: {request.module}."
        full_prompt = f"{instruction}\nSavol: {request.message}"
        response = model.generate_content(full_prompt)
        return {"answer": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"answer": f"Xato: {str(e)}"})