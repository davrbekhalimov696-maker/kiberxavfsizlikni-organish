import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Yo'llarni dinamik aniqlash
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")

# Papka mavjudligini tekshirish, agar yo'q bo'lsa xato bermasligi uchun
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    templates = Jinja2Templates(directory=static_path)
else:
    # Agar static papkasi topilmasa, asosiy direktoriya bilan ishlashga urinish
    templates = Jinja2Templates(directory=BASE_DIR)

# Gemini AI (404 xatosini oldini olish uchun barqaror model)
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

class ChatRequest(BaseModel):
    message: str
    lang: str = "uz"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception:
        return HTMLResponse("index.html topilmadi. Iltimos, fayl joylashuvini tekshiring.")

@app.post("/ask")
async def ask_ai(request: ChatRequest):
    try:
        response = model.generate_content(request.message)
        return {"answer": response.text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"answer": f"Xato: {str(e)}"})