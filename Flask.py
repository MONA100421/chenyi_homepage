from flask import Flask, render_template, request
from flask_mail import Mail, Message
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)

# 配置郵件設置
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-password'

mail = Mail(app)

app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

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

if __name__ == '__main__':
    app.run(debug=True)
