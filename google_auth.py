from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import os
import json

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)

        # 🔥 This saves the token as JSON, not pickle
        with open('token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    # Quick test
    service = build('calendar', 'v3', credentials=creds)
    events_result = service.events().list(calendarId='primary').execute()
    print("✅ Calendar access successful")

if __name__ == '__main__':
    main()
