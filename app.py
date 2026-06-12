from flask import Flask
import pymysql
import os

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')
DB_NAME = os.environ.get('DB_NAME', 'Myapp_base')

@app.route('/')
def hello():
    try:
        connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
        return "Успешное подключение к базе данных Myapp_base!"
    except Exception as e:
        return f"Ошибка подключения к БД: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)