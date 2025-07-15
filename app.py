import os
from flask import Flask, render_template, request
import requests
import secrets
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

# Mock authentication
VALID_TOKEN = secrets.token_urlsafe(16)  # Generate a secure random token
print(f"Generated token: {VALID_TOKEN}")  # For debugging
USERS = {"testuser": VALID_TOKEN}

# Typebot API config
TYPEBOT_API_TOKEN = os.getenv("TYPEBOT_API_TOKEN", "abc12345")
TYPEBOT_WORKSPACE_ID = os.getenv("TYPEBOT_WORKSPACE_ID", "xyz12345")
API_BASE_URL = "https://app.typebot.io/api/v1"



def bridge_to_typebot_auth(app_token):
    """Mock bridging: Maps app token to Typebot API token."""
    return TYPEBOT_API_TOKEN if app_token in USERS.values() else None

def get_typebot_bots():
    """Fetch list of Typebot bots from API"""
    url = f"{API_BASE_URL}/typebots?workspaceId={TYPEBOT_WORKSPACE_ID}"
    headers = {"Authorization": f"Bearer {TYPEBOT_API_TOKEN}"}
    
    response = requests.get(url, headers=headers)
    return response.json().get("typebots", []) if response.status_code == 200 else []

def get_typebot_public_id(bot_id):
    """Fetch public ID of a Typebot bot"""
    url = f"{API_BASE_URL}/typebots/{bot_id}"
    headers = {"Authorization": f"Bearer {TYPEBOT_API_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("typebot", {}).get("publicId")
    return None



@app.route('/')
def home():
    token = request.args.get('token')
    if not bridge_to_typebot_auth(token):
        return "Unauthorized. Provide valid token.", 401

    bots = get_typebot_bots()
    return render_template('index.html', token=token, bots=bots)

@app.route('/embed/<bot_id>')
def embed_bot(bot_id):
    token = request.args.get('token')
    if not bridge_to_typebot_auth(token):
        return "Unauthorized. Provide valid token.", 401
    
    bot_public_id = get_typebot_public_id(bot_id)
    if not bot_public_id:
        return "Bot not found or unauthorized.", 404
    return render_template('embed.html', bot_id=bot_public_id, token=token)

@app.route('/analytics/<bot_id>')
def get_analytics(bot_id):
    token = request.args.get('token')
    if not bridge_to_typebot_auth(token):
        return "Unauthorized. Provide valid token.", 401

    results_url = f"{API_BASE_URL}/typebots/{bot_id}/results?limit=50&timeFilter=last7Days"
    headers = {"Authorization": f"Bearer {TYPEBOT_API_TOKEN}"}
    
    response = requests.get(results_url, headers=headers)
    results = response.json().get("results", [])
    
    total_sessions = len(results)
    usage_stats = sum(1 for r in results if r.get("isCompleted", False))
    last_run = max((r.get("createdAt") for r in results), default="N/A")
    
    return render_template('analytics.html',
                           total_sessions=total_sessions,
                           usage_stats=usage_stats,
                           last_run=last_run,
                           bot_id=get_typebot_public_id(bot_id),
                           token=token)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)