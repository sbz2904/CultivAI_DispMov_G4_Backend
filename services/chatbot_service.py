import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def ask_chatbot(message, weather_data):
    context = f"""
    Actualmente, en tu ubicación ({weather_data.get('name', 'desconocida')}),
    la temperatura es de {weather_data.get('main', {}).get('temp', 'desconocida')}°C,
    la humedad es del {weather_data.get('main', {}).get('humidity', 'desconocida')}%,
    y el clima se describe como "{weather_data.get('weather', [{}])[0].get('description', 'desconocido')}".
    Solo responde preguntas relacionadas con la agricultura.
    """
    
    prompt = f"{context}\nPregunta del usuario: {message}"
    
    try:
        result = model.generate_content([prompt])
        if not hasattr(result, 'text'):
            return {"response": "No se pudo obtener una respuesta válida."}
        
        return {"response": result.text.strip()}
    except Exception as e:
        return {"error": str(e)}
