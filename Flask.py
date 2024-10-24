from flask import Flask, render_template, request
from flask_mail import Mail, Message
from flask_cors import CORS
import requests
import feedparser
import os

app = Flask(__name__)
CORS(app)

# 配置郵件設置
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    fullname = request.form['fullname']
    email = request.form['email']
    message = request.form['message']

    # 創建郵件
    msg = Message("New Form Submission",
                  sender="your-email@example.com",
                  recipients=["recipient-email@example.com"])
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

    return render_template('contact.html', weather=weather_info, news=news_info)

def get_weather(city):
    api_key = '51b40e906ccaf0b4db4ba1ad7638e185'  # OpenWeather API Key
    base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(base_url)
    data = response.json()
    
    if data["cod"] != "404":
        main = data["main"]
        weather_desc = data["weather"][0]["description"]
        temperature = main["temp"]
        return f"City: {city}\nTemperature: {temperature}°C\nWeather: {weather_desc}"
    else:
        return "City not found."

def get_latest_news():
    url = "https://news.google.com/rss"
    news_feed = feedparser.parse(url)

    articles = []
    for entry in news_feed.entries[:5]:  # 只顯示前 5 篇新聞
        title = entry.title
        link = entry.link
        articles.append(f"{title}\nRead more: {link}\n")

    return "\n".join(articles)

if __name__ == '__main__':
    app.run(debug=True)
