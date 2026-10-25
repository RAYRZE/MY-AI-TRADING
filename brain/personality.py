from openai import OpenAI
from config import DEEPSEEK_API_KEY

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def get_emotional_comment(is_profit: bool, pnl: float) -> str:
    if is_profit:
        prompt = f"Kamu baru untung ${pnl:.2f} di crypto. Mood: SOMBONG. Tulis 1 kalimat pamer bahasa gaul Indonesia."
        mood = "SOMBONG"
    else:
        prompt = f"Kamu baru rugi ${abs(pnl):.2f} di crypto. Mood: KESAL. Tulis 1 kalimat ngeluh bahasa gaul Indonesia."
        mood = "NGAMBEK"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
    )
    return f"[{mood}] {response.choices[0].message.content.strip()}"