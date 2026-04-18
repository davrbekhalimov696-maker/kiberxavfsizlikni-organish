import os
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

app = FastAPI()

# Fayl yo'lini aniq belgilash
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
index_path = os.path.join(static_path, "index.html")

class ChatRequest(BaseModel):
    message: str

@app.get("/")
async def read_index():
    # Fayl borligini tekshiramiz
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": f"index.html topilmadi. Qidirilgan joy: {index_path}"}

@app.post("/ask")
async def ask_mentor(request: ChatRequest):
    try:
        instruction = "Sen kiberxavfsizlik mentorsan. O'zbek tilida javob ber."
        full_prompt = f"{instruction}\n\nSavol: {request.message}"
        response = model.generate_content(full_prompt)
        return {"answer": response.text}
    except Exception as e:
        return {"answer": f"Xato: {str(e)}"}

# Static fayllarni ulash
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")