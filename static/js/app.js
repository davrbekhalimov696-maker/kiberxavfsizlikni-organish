async function loadLesson(name) {
    const res = await fetch(`/api/lesson/${name}`);
    const data = await res.json();

    document.getElementById('welcome-msg').style.display = 'none';
    document.getElementById('lesson-content').style.display = 'block';

    document.getElementById('lesson-title').innerText = data.title;
    document.getElementById('lesson-desc').innerText = data.desc;
    document.getElementById('code-text').innerText = data.code;
}

function copyCode() {
    const text = document.getElementById('code-text').innerText;
    navigator.clipboard.writeText(text);
    alert("Kod nusxalandi! Endi uni terminalga qo'yishingiz mumkin.");
}