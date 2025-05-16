from flask import Flask
from models import app  # используем тот же объект app

@app.route('/')
def home():
    return 'Flask работает! 🟢'

if __name__ == '__main__':
    app.run(debug=True)
