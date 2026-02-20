from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
import os
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

CLIENT_ID = '611341589784-rq5808l4jp6ro59d5qnt5dc1aat4vsdv.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'https://calendar-miniapp.onrender.com/auth/google/callback'
SCOPES = 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/userinfo.email openid'

# Хранилище токенов (в продакшене используйте базу данных)
user_tokens = {}

@app.route('/debug')
def debug():
    return f'''
    <h1>DEBUG INFO</h1>
    <p>CLIENT_ID: {CLIENT_ID}</p>
    <p>CLIENT_SECRET length: {len(CLIENT_SECRET)}</p>
    <p>REDIRECT_URI: {REDIRECT_URI}</p>
    <p>SCOPES: {SCOPES}</p>
    <p>Connected users: {len(user_tokens)}</p>
    '''

@app.route('/')
@app.route('/health')
def health():
    return 'OK', 200

@app.route('/auth/google')
def auth_google():
    user_id = request.args.get('user_id', 'test')
    chat_id = request.args.get('chat_id', 'test')
    auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPES}&response_type=code&state={user_id}|{chat_id}&access_type=offline&prompt=consent"
    return redirect(auth_url)

@app.route('/auth/google/callback')
def auth_callback():
    code = request.args.get('code')
    state = request.args.get('state', 'test|test')
    
    if code:
        token_data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI
        }
        token_response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
        token_json = token_response.json()
        
        if 'access_token' in token_json:
            # Сохраняем токен
            user_id = state.split('|')[0]
            user_tokens[user_id] = {
                'access_token': token_json['access_token'],
                'refresh_token': token_json.get('refresh_token'),
                'expires_at': datetime.now() + timedelta(seconds=token_json.get('expires_in', 3600))
            }
            
            return f'''
            <html>
            <head><title>Success</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>✅ Google Calendar подключен!</h1>
                <p>Теперь вы можете создавать события.</p>
                <p>Можете закрыть это окно.</p>
                <script>
                    if (window.opener) {{
                        window.opener.postMessage('google_connected', '*');
                    }}
                    setTimeout(() => window.close(), 3000);
                </script>
            </body>
            </html>
            '''
        else:
            return f'<h1>❌ Ошибка</h1><p>{token_json}</p>', 400
    
    return '❌ ERROR: No code', 400

@app.route('/auth/status/<user_id>')
def auth_status(user_id):
    if user_id in user_tokens:
        token_data = user_tokens[user_id]
        if datetime.now() < token_data['expires_at']:
            return jsonify({'connected': True})
    return jsonify({'connected': False})

@app.route('/create_event', methods=['POST'])
def create_event():
    data = request.json
    user_id = data.get('user_id', 'test')
    
    # Проверяем токен
    if user_id not in user_tokens:
        return jsonify({'error': 'Not authorized. Please connect Google Calendar first.'}), 401
    
    token_data = user_tokens[user_id]
    access_token = token_data['access_token']
    
    # Данные события
    title = data.get('title', 'Meeting')
    start_datetime = data.get('datetime')  # формат: "2026-02-10T14:00:00"
    duration = data.get('duration', 30)  # минуты
    attendee = data.get('attendee', '')
    
    # Парсим время
    try:
        start = datetime.fromisoformat(start_datetime)
        end = start + timedelta(minutes=duration)
    except:
        return jsonify({'error': 'Invalid datetime format'}), 400
    
    # Формируем событие для Google Calendar
    event = {
        'summary': title,
        'start': {
            'dateTime': start.isoformat(),
            'timeZone': 'Europe/Moscow',
        },
        'end': {
            'dateTime': end.isoformat(),
            'timeZone': 'Europe/Moscow',
        },
    }
    
    # Добавляем участника если указан
    if attendee and '@' in attendee:
        event['attendees'] = [{'email': attendee}]
    
    # Отправляем в Google Calendar API
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.post(
        'https://www.googleapis.com/calendar/v3/calendars/primary/events',
        headers=headers,
        json=event
    )
    
    if response.status_code == 200 or response.status_code == 201:
        event_data = response.json()
        return jsonify({
            'success': True,
            'event_id': event_data.get('id'),
            'html_link': event_data.get('htmlLink'),
            'message': 'Event created successfully!'
        })
    else:
        error_data = response.json()
        # Если токен истёк — удаляем его
        if response.status_code == 401:
            del user_tokens[user_id]
            return jsonify({'error': 'Token expired. Please reconnect Google Calendar.'}), 401
        return jsonify({'error': error_data}), response.status_code

@app.route('/get_events', methods=['GET'])
def get_events():
    user_id = request.args.get('user_id', 'test')
    
    if user_id not in user_tokens:
        return jsonify({'error': 'Not authorized'}), 401
    
    token_data = user_tokens[user_id]
    access_token = token_data['access_token']
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    # Получаем события на ближайшую неделю
    now = datetime.utcnow().isoformat() + 'Z'
    time_max = (datetime.utcnow() + timedelta(days=7)).isoformat() + 'Z'
    
    response = requests.get(
        f'https://www.googleapis.com/calendar/v3/calendars/primary/events?timeMin={now}&timeMax={time_max}&singleEvents=true&orderBy=startTime',
        headers=headers
    )
    
    if response.status_code == 200:
        events = response.json().get('items', [])
        return jsonify({'events': events})
    else:
        return jsonify({'error': 'Failed to fetch events'}), response.status_code

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
