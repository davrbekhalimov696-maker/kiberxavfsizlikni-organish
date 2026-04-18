import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Yo'llarni aniq belgilash (Xatolikni tuzatish)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")

# Statik ulanish
app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=static_dir)

# O'quv darslari bazasi
DATABASE = {
    "linux": {
        "title": "Linux Terminali",
        "desc": "Kiberxavfsizlikda terminal bilan ishlash eng asosiy ko'nikmadir. Quyida eng ko'p ishlatiladigan buyruqlar keltirilgan.",
        "image": "/static/images/linux.png",
        "code": "# Fayllarni ko'rish\nls -la\n\n# Papka yaratish\nmkdir cyber_lab\n\n# Huquqlarni o'zgartirish\nchmod +x script.sh"
    },
    "nmap": {
        "title": "Nmap: Tarmoq Skanerlash",
        "desc": "Nmap yordamida ochiq portlarni va xizmatlarni aniqlash mumkin. Bu razvedka bosqichining asosi hisoblanadi.",
        "image": "/static/images/nmap.png",
        "code": "# Oddiy skanerlash\nnmap 192.168.1.1\n\n# Xizmatlar versiyasini aniqlash\nnmap -sV target.com\n\n# Barcha portlarni tekshirish\nnmap -p- 10.10.10.1"
    },
    "metasploit": {
        "title": "Metasploit Framework",
        "desc": "Eksploitlar bilan ishlash uchun eng mashhur platforma. Unda minglab tayyor zaifliklar mavjud.",
        "image": "/static/images/msf.png",
        "code": "# Konsolni ishga tushirish\nmsfconsole\n\n# Eksploit qidirish\nsearch eternalblue\n\n# Eksploitni tanlash\nuse exploit/windows/smb/ms17_010_eternalblue"
    }
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/lesson/{name}")
async def get_lesson(name: str):
    if name not in DATABASE:
        raise HTTPException(status_code=404)
    return DATABASE[name]