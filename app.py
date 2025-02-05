from flask import Flask
from routes.user_routes import user_bp
from routes.sembrio_routes import sembrio_bp
from routes.weather_routes import weather_bp
from routes.chatbot_routes import chatbot_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_jwt_secret_key'

# Registrar Blueprints
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(sembrio_bp, url_prefix='/api/sembrios')   
app.register_blueprint(weather_bp, url_prefix='/api/weather')
app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
