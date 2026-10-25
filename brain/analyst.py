from openai import OpenAI
from config import DEEPSEEK_API_KEY

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def get_signal(price: float, symbol: str) -> str:
    prompt = f"""
    Harga {symbol} saat ini adalah ${price}.
    Berikan sinyal trading: LONG (beli), SHORT (jual), atau HOLD.
    Jawab HANYA dengan satu kata: LONG, SHORT, atau HOLD.
    """
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=10
    )
    answer = response.choices[0].message.content.strip().upper()
    return answer if answer in ["LONG", "SHORT", "HOLD"] else "HOLD"