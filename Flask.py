from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    fullname = request.form['fullname']
    email = request.form['email']
    message = request.form['message']
    
    # 這裡可以將數據存入數據庫或發送到 Google Sheets
    print(f"Received: {fullname}, {email}, {message}")
    
    return "Form submitted successfully!"

if __name__ == '__main__':
    app.run(debug=True)
