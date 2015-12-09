import praw
import requests
import time

# Account settings (private)
USERNAME = ''
PASSWORD = ''

# OAuth settings (private)
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://127.0.0.1:65010/authorize_callback'

# Configuration Settings
USER_AGENT = ""
AUTH_TOKENS = ["identity","read"]
EXPIRY_BUFFER = 60

def get_session_data():
    response = requests.post("https://www.reddit.com/api/v1/access_token",
      auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
      data = {"grant_type": "password", "username": USERNAME, "password": PASSWORD},
      headers = {"User-Agent": USER_AGENT})
    response_dict = dict(response.json())
    response_dict['retrieved_at'] = time.time()
    return response_dict

def get_praw():
    r = praw.Reddit(USER_AGENT)
    r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    session_data = get_session_data()
    r.set_access_credentials(set(AUTH_TOKENS), session_data['access_token'])
    return (r, session_data)

def main(r, session_data):
    EXPIRES_AT = session_data['retrieved_at'] + session_data['expires_in']
    # While True: # (Goes here if program runs constantly)
    if time.time() >= EXPIRES_AT - EXPIRY_BUFFER:
        raise praw.errors.OAuthInvalidToken
    ##### MAIN CODE #####

if __name__ == "__main__":
    while True:
        try:
            print("Retrieving new OAuth token...")
            main(*get_praw())
        except praw.errors.OAuthInvalidToken:
            print("OAuth token expired.")
        except praw.errors.HTTPException:
            print("HTTP error. Retrying in 10...")
            time.sleep(10)
