@app.route('/auth/google')
def auth_google():
    print(f"DEBUG: CLIENT_ID={CLIENT_ID}")
    print(f"DEBUG: REDIRECT_URI={REDIRECT_URI}")
    print(f"DEBUG: SCOPES={SCOPES}")
    
    user_id = request.args.get('user_id', 'unknown')
    chat_id = request.args.get('chat_id', '')
    
    # остальной код..
from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# Получаем из environment variables Railway
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')


# Scopes для Google Calendar
SCOPES = 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/userinfo.email openid'
REDIRECT_URI = 'https://2-production-9efb.up.railway.app/auth/google/callback'
# Временное хранилище токенов (в продакшене используй БД)
user_tokens = {}

@app.route('/')
def home():
    return 'CalendarBot Backend is running! 🚀'

@app.route('/auth/google')
def auth_google():
    user_id = request.args.get('user_id', 'unknown')
    chat_id = request.args.get('chat_id', '')
    
    # Строим URL для авторизации Google
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={SCOPES}"
        f"&access_type=offline"
        f"&prompt=consent"
        f"&state={user_id}:{chat_id}"
    )
    
    return redirect(auth_url)

@app.route('/auth/google/callback')
def google_callback():
    code = request.args.get('code')
    state = request.args.get('state', '')
    
    if not code:
        return 'Error: No authorization code received', 400
    
    # Извлекаем user_id из state
    user_id = state.split(':')[0] if ':' in state else 'unknown'
    
    # Обмениваем code на access_token
    token_response = requests.post('https://oauth2.googleapis.com/token', data={
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    })
    
    tokens = token_response.json()
    
    if 'error' in tokens:
        return f"Error from Google: {tokens.get('error_description', tokens['error'])}", 400
    
    # Сохраняем токены (в продакшене - в БД)
    user_tokens[user_id] = {
        'access_token': tokens.get('access_token'),
        'refresh_token': tokens.get('refresh_token'),
        'expires_in': tokens.get('expires_in')
    }
    
    print(f"✅ User {user_id} connected! Tokens saved.")
    
    # Редирект обратно в Telegram Mini App
    return '''
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Connected!</title>
        <style>
            body {
                font-family: -apple-system, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
            }
            .card {
                background: white;
                color: #333;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 { margin: 0 0 10px; font-size: 32px; }
            p { margin: 0; opacity: 0.7; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>✅ Connected!</h1>
            <p>You can close this window and return to Telegram.</p>
        </div>
        <script>
            // Попытка закрыть окно (работает не во всех браузерах)
            setTimeout(() => {
                window.close();
            }, 2000);
        </script>
    </body>
    </html>
    '''

@app.route('/save_meetings', methods=['POST'])
def save_meetings():
    data = request.json
    print('Meetings saved:', data)
    return jsonify({'status': 'ok'})

@app.route('/get_calendar_events')
def get_calendar_events():
    user_id = request.args.get('user_id')
    
    if user_id not in user_tokens:
        return jsonify({'error': 'Not connected'}), 401
    
    access_token = user_tokens[user_id]['access_token']
    
    # Запрос событий из Google Calendar
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(
        'https://www.googleapis.com/calendar/v3/calendars/primary/events',
        headers=headers,
        params={'maxResults': 10, 'orderBy': 'startTime', 'singleEvents': True}
    )
    
    if response.status_code == 401:
        return jsonify({'error': 'Token expired'}), 401
    
    return jsonify(response.json())

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
