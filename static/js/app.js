let currentLang = 'uz';

async function setLanguage(lang) {
    currentLang = lang;
    document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
    // Tugma holatini yangilash logikasi bu yerda
}

async function loadModule(moduleName) {
    const response = await fetch(`/api/module/${moduleName}?lang=${currentLang}`);
    const data = await response.json();

    document.getElementById('module-title').innerText = data.title;
    document.getElementById('theory-text').innerText = data.theory;
    document.getElementById('video-frame').src = data.video;
}

async function askMentor() {
    const input = document.getElementById('user-input').value;
    const response = await fetch('/ask', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ message: input, lang: currentLang })
    });
    const result = await response.json();
    document.getElementById('ai-response').innerText = result.answer;
}