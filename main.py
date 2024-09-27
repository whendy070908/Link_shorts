from flask import Flask, request, jsonify, render_template_string, make_response
import sqlite3
import string
import random

domain = "" #본인의 도메인
app = Flask(__name__)

def init_db():
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS urls (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            short_url TEXT UNIQUE,
                            original_url TEXT
                        )''')
        conn.commit()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

def store_url(original_url):
    short_url = generate_short_url()
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO urls (short_url, original_url) VALUES (?, ?)", (short_url, original_url))
        conn.commit()
    return short_url

@app.errorhandler(404)
def page_not_found(e):
    html_content = '''
        <html lang="ko">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>404 - 페이지를 찾을 수 없습니다</title>
                <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
                <style>
                    body, html {
                        height: 100%;
                        margin: 0;
                        font-family: 'Poppins', sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
                        color: white;
                    }
                    .container {
                        text-align: center;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 40px;
                        background-color: rgba(255, 255, 255, 0.1);
                        border-radius: 15px;
                        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                        animation: fadeIn 1.5s ease-in-out;
                    }
                    h1 {
                        font-size: 96px;
                        margin: 0;
                        font-weight: 700;
                    }
                    p {
                        font-size: 24px;
                        margin: 20px 0;
                    }
                    a {
                        text-decoration: none;
                        color: white;
                        font-weight: 600;
                        padding: 12px 24px;
                        border: 2px solid white;
                        border-radius: 8px;
                        transition: background-color 0.3s, color 0.3s;
                    }
                    a:hover {
                        background-color: white;
                        color: #3498db;
                    }
                    @keyframes fadeIn {
                        from {
                            opacity: 0;
                            transform: scale(0.9);
                        }
                        to {
                            opacity: 1;
                            transform: scale(1);
                        }
                    }
                    footer {
                        margin-top: 20px;
                        font-size: 14px;
                        color: rgba(255, 255, 255, 0.8);
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>404</h1>
                    <p>찾고 있는 페이지가 존재하지 않습니다.</p>
                    <a href="https://koreanbots.dev/bots/1249261458928173106">봇 초대하기</a>
                    <footer>
                        © 2024 Discord Mezbot KR | All rights reserved.
                    </footer>
                </div>
            </body>
        </html>
    '''
    response = make_response(html_content, 404)
    return response

@app.route('/<short_url>')
def redirect_to_original(short_url):
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_url FROM urls WHERE short_url = ?", (short_url,))
        row = cursor.fetchone()

    if row:
        original_url = row[0]
        return render_template_string('''
            <html lang="ko">
                <head>
                    <meta charset="UTF-8">
                    <title>리디렉션 중...</title>
                    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
                    <style>
                        body {
                            font-family: 'Poppins', sans-serif;
                            display: flex;
                            flex-direction: column;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                            background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
                        }
                        .container {
                            text-align: center;
                            padding: 40px;
                            background-color: white;
                            border-radius: 15px;
                            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
                            animation: fadeIn 1s ease-in-out;
                        }
                        h1 {
                            font-size: 28px;
                            color: #333;
                            font-weight: 600;
                        }
                        p {
                            font-size: 18px;
                            color: #555;
                        }
                        a {
                            text-decoration: none;
                            color: #3498db;
                            font-weight: 600;
                        }
                        a:hover {
                            text-decoration: none;
                        }
                        #countdown {
                            font-size: 22px;
                            font-weight: 600;
                            color: #e74c3c;
                        }
                        @keyframes fadeIn {
                            from {
                                opacity: 0;
                                transform: translateY(20px);
                            }
                            to {
                                opacity: 1;
                                transform: translateY(0);
                            }
                        }
                        .bot-button {
                            display: inline-block;
                            padding: 12px 24px;
                            margin-top: 20px;
                            font-size: 16px;
                            font-weight: 600;
                            color: white;
                            background-color: #3498db;
                            border: none;
                            border-radius: 8px;
                            cursor: pointer;
                            text-decoration: none;
                            transition: background-color 0.3s ease;
                        }
                        .bot-button:hover {
                            background-color: #2980b9;
                            text-decoration: none;
                        }
                        footer {
                            margin-top: 20px;
                            font-size: 14px;
                            color: #333;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>잠시만 기다려 주세요!</h1>
                        <p id="countdown">5초 후에 <a href="{{ original_url }}">원래 페이지</a>로 이동합니다.</p>
                        <p>혹시 자동으로 이동하지 않으면 <a href="{{ original_url }}">여기</a>를 클릭해 주세요.</p>
                        <a href="https://koreanbots.dev/bots/1249261458928173106" class="bot-button">봇 초대하기</a>
                        <footer>
                            © 2024 Discord Mezbot KR | All rights reserved.
                        </footer>
                    </div>

                    <script>
                        var countdownElement = document.getElementById('countdown');
                        var secondsLeft = 5;

                        function updateCountdown() {
                            if (secondsLeft > 0) {
                                countdownElement.innerHTML = secondsLeft + "초 후에 <a href='{{ original_url }}'>원래 페이지</a>로 이동합니다.";
                                secondsLeft--;
                            } else {
                                window.location.href = "{{ original_url }}";
                            }
                        }

                        setInterval(updateCountdown, 1000);
                    </script>
                </body>
            </html>
        ''', original_url=original_url)
    else:
        return page_not_found(404)

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.json.get('url')
    short_url = store_url(original_url)
    return jsonify({"short_url": f"{domain}/{short_url}"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
