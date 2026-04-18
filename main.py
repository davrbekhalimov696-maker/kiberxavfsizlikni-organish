import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from pydantic import BaseModel
from dotenv import load_dotenv

# Environment variables yuklash
load_dotenv()

app = FastAPI(title="CyberZone Pro Platform")

# Fayl yo'llarini Render uchun to'g'rilash
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")

# Papka mavjudligini tekshirish (Xatolikni oldini olish uchun)
if not os.path.exists(static_path):
    os.makedirs(static_path)
    os.makedirs(os.path.join(static_path, "css"))
    os.makedirs(os.path.join(static_path, "js"))

# Statik va shablonlar ulanishi
app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=static_path)

# Gemini AI sozlamalari
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class ChatRequest(BaseModel):
    message: str
    lang: str = "uz"
    module: str = "general"

# O'quv bazasi
CYBER_CONTENT = {
    "kiberetika": {
        "uz": {"title": "Kiberetika", "theory": "Hakerlikning axloqiy me'yorlari...", "video": "https://www.youtube.com/embed/example1"},
        "en": {"title": "Cyber Ethics", "theory": "Ethical standards of hacking...", "video": "https://www.youtube.com/embed/example2"}
    },
    "kibertahlil": {
        "uz": {"title": "Kibertahlil", "theory": "Tahdidlarni aniqlash va tahlil qilish...", "video": "https://www.youtube.com/embed/example3"},
        "en": {"title": "Cyber Analysis", "theory": "Threat detection and analysis...", "video": "https://www.youtube.com/embed/example4"}
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
        prompt = f"Sen kiberxavfsizlik mentorsan. Til: {request.lang}. Mavzu: {request.module}. Savol: {request.message}"
        response = model.generate_content(prompt)
        return {"answer": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"answer": f"Xato: {str(e)}"})