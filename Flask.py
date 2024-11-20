from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import os
import logging

# 配置日誌記錄
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加載環境變量
load_dotenv()  # 確保 .env 文件中的 API 金鑰等被加載

app = Flask(__name__, static_folder='assets')
CORS(app)  # 允許跨域請求

# 一次性讀取 API 金鑰
api_key = os.environ.get('OPENWEATHER_API_KEY')
if not api_key:
    logger.error("API key not found in environment variables.")

# 配置郵件設置
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

# 天氣數據函數
def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 檢查是否有錯誤的狀態碼
        data = response.json()
        print(f"API Response Data: {data}")
        
        # 檢查 API 返回的狀態碼是否為 200
        if data.get('cod') != 200:
            return None

        # 返回天氣數據
        return {
            'city': data['name'],
            'temperature': round(data['main']['temp']),
            'description': data['weather'][0]['description']
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching weather data: {e}")
        return None

# 網站首頁處理路由
@app.route('/', methods=['GET'])
def home():
    city = 'Los Angeles'  # 預設顯示洛杉磯的天氣
    weather_data = fetch_weather_data(city)
    return render_template('index.html', weather=weather_data)

# 用於獲取天氣數據的 POST 路由
@app.route('/get_weather', methods=['POST'])
def get_weather():
    try:
        city = request.get_json().get('city')
        if not city:
            return jsonify({'error': 'City not provided'}), 400
        
        weather_data = fetch_weather_data(city)
        
        if not weather_data:
            return jsonify({'error': f'Wow, you sure {city} is on Earth?'}), 400
        
        return jsonify({'weather': weather_data})
    except Exception as e:
        logger.error(f"Error in /get_weather: {e}")
        return jsonify({'error': 'An error occurred while fetching weather data.'}), 500

# 聯絡表單提交處理路由
@app.route('/submit', methods=['POST'])
def submit():
    fullname = request.form['fullname']
    email = request.form['email']
    message = request.form['message']

    # 創建郵件
    msg = Message("New Form Submission",
                  sender=app.config['MAIL_USERNAME'],
                  recipients=["she050623@gmail.com"])  # 改成你的收件人 email
    msg.body = f"Fullname: {fullname}\nEmail: {email}\nMessage: {message}"
    mail.send(msg)

    return "Form submitted successfully and email sent!"

# 聯絡頁面處理路由
@app.route('/contact')
def contact():
    city = "Los Angeles"
    weather_info = fetch_weather_data(city)

    # 渲染 contact.html 模板
    return render_template('contact.html', weather=weather_info)

# 主程序
if __name__ == '__main__':
    app.run(debug=True)
