from flask import Flask, request, redirect, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

CLIENT_ID = '611341589784-rq5808l4jp6ro59d5qnt5dc1aat4vsdv.apps.googleusercontent.com'
CLIENT_SECRET = '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'  
REDIRECT_URI = 'https://calendar-miniapp.onrender.com/auth/google/callback'
SCOPES = 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/userinfo.email openid'


@app.route('/debug')
def debug():
    return f'''
    <h1>DEBUG INFO</h1>
    <p>CLIENT_ID: {CLIENT_ID}</p>
    <p>CLIENT_SECRET length: {len(CLIENT_SECRET)}</p>
    <p>REDIRECT_URI: {REDIRECT_URI}</p>
    <p>SCOPES: {SCOPES}</p>
    '''

@app.route('/')
@app.route('/health')
def health():
    return 'OK', 200

@app.route('/auth/google')
def auth_google():
    user_id = request.args.get('user_id', 'test')
    chat_id = request.args.get('chat_id', 'test')
    auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope={SCOPES}&response_type=code&state={user_id}|{chat_id}"
    print(f"DEBUG auth_url={auth_url[:200]}...")
    return redirect(auth_url)

@app.route('/auth/google/callback')
def auth_callback():
    code = request.args.get('code')
    state = request.args.get('state')
    print(f"DEBUG callback code={code}")
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
        print(f"DEBUG token={token_json}")
        return f'<h1>✅ SUCCESS!</h1><p>{token_json}</p><script>setTimeout(()=>window.close(),5000);</script>'
    return '❌ ERROR', 400

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
