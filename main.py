from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# ХАРДКОД — ТВОЙ НОВЫЙ CLIENT
CLIENT_ID = '611341589784-shq8uft9k868743ejp1vcb484vejsb6f.apps.googleusercontent.com'
CLIENT_SECRET = 'GOCSPX-твой_секрет_Web_client_2'  # ← Обязательно замени!
REDIRECT_URI = 'https://2-production-9efb.up.railway.app/auth/google/callback'
SCOPES = 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/userinfo.email openid'

print(f"DEBUG: CLIENT_ID={CLIENT_ID}")  # Лог для проверки
print(f"DEBUG: REDIRECT_URI={REDIRECT_URI}")

@app.route('/')
@app.route('/health')
def health():
    return 'OK', 200

@app.route('/auth/google')
def auth_google():
    user_id = request.args.get('user_id', 'test')
    chat_id = request.args.get('chat_id', 'test')
    auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPES}&response_type=code&state={user_id}|{chat_id}"
    print(f"DEBUG: auth_url={auth_url}")  # Лог URL
    return redirect(auth_url)

@app.route('/auth/google/callback')
def auth_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    print(f"DEBUG: code={code}, state={state}")
    if code:
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI
        }
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()
        print(f"DEBUG: token_response={token_json}")
        return f'''
        <html><body>
        <h1>✅ Авторизация успешна!</h1>
        <p>Token: {token_json}</p>
        <p>State: {state}</p>
        <script>setTimeout(() => {{window.close()}}, 5000);</script>
        </body></html>
        '''
    return '❌ Ошибка авторизации', 400

@app.route('/save_meetings', methods=['POST'])
def save_meetings():
    data = request.json
    print('Meetings saved:', data)
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)

print(f"DEBUG SECRET LENGTH: {len(CLIENT_SECRET)}")  # Должно >40

