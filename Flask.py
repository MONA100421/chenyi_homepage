from flask import Flask, render_template, request
from flask_mail import Mail, Message
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import feedparser
import os

load_dotenv()  # 加載 .env 文件

app = Flask(__name__, static_folder='assets')
CORS(app)

# 配置郵件設置
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

def fetch_weather_data():
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    city = 'Los Angeles'  # 這可以根據用戶輸入進行動態設置
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果狀態碼不是 200，則拋出錯誤
        data = response.json()
        return {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description']
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    city = 'Los Angeles'  # Default city
    if request.method == 'POST':
        city = request.form.get('city')  # Get city from the form
    weather_data = fetch_weather_data(city)  # Pass city to the function
    if not weather_data:
        return "Error fetching weather data", 500
    return render_template('index.html', weather=weather_data)

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

@app.route('/contact')
def contact():
    # 獲取天氣資訊
    city = "Los Angeles"
    weather_info = get_weather(city)
    
    # 獲取最新新聞
    news_info = get_latest_news()

    # 渲染 contact.html 模板，並將天氣與新聞資料傳遞過去
    return render_template('contact.html', weather=weather_info, news=news_info)

def get_weather(city):
    api_key = os.environ.get('OPENWEATHER_API_KEY')  # 將 API 金鑰儲存在 .env 文件中
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(base_url)
    data = response.json()
    print(data)  # 打印天氣 API 響應數據
    
    if data["cod"] != "404":
        main = data["main"]
        weather_desc = data["weather"][0]["description"]
        temperature = main["temp"]
        return {
            "city": city,
            "temperature": f"{temperature}°C",
            "description": weather_desc
        }
    else:
        return {
            "city": city,
            "temperature": "N/A",
            "description": "City not found."
        }


def get_latest_news():
    url = "https://news.google.com/rss"
    news_feed = feedparser.parse(url)

    articles = []
    for entry in news_feed.entries[:5]:  # 只顯示前 5 篇新聞
        articles.append({
            "title": entry.title,
            "link": entry.link
        })

    return articles

if __name__ == '__main__':
    app.run(debug=True)
