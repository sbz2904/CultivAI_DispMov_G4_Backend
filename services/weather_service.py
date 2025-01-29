import requests

API_KEY = '1e53941ecd82227342e548ec70553384'

def get_weather(latitude, longitude):
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {'error': str(e)}
