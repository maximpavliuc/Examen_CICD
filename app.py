from flask import Flask, request, redirect, url_for
import pymysql
import os
import time

app = Flask(__name__)

DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root_password')
DB_NAME = os.environ.get('DB_NAME', 'Myapp_base')

def get_connection():
    for _ in range(15):
        try:
            return pymysql.connect(
                host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
            )
        except:
            time.sleep(3)
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_connection()
    if not conn:
        return "<h1>Ошибка: Не удалось подключиться к базе данных.</h1>", 500

    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                content VARCHAR(255)
            )
        """)
        conn.commit()

        if request.method == 'POST':
            new_text = request.form.get('user_text')
            if new_text:
                cursor.execute("INSERT INTO notes (content) VALUES (%s)", (new_text,))
                conn.commit()
            return redirect(url_for('index'))

        cursor.execute("SELECT * FROM notes")
        records = cursor.fetchall()
    
    conn.close()

    html = "<h2>База данных Myapp_base</h2>"
    
    html += "<form method='post' style='margin-bottom: 20px;'>"
    html += "  <input type='text' name='user_text' placeholder='Введите текст...' required style='padding: 5px; width: 250px;'>"
    html += "  <button type='submit' style='padding: 5px 10px;'>Добавить в БД</button>"
    html += "</form>"

    html += "<table border='1' cellpadding='8' style='border-collapse: collapse; text-align: left; width: 400px;'>"
    html += "<tr style='background-color: #f2f2f2;'><th>ID</th><th>Сохраненный текст</th></tr>"
    
    for row in records:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td></tr>"
    
    html += "</table>"

    return html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)