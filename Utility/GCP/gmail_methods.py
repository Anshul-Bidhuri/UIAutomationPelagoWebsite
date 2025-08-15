from email.mime.text import MIMEText
import base64, os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from Helpers import custom_logger

log = custom_logger.get_logger()

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

credentials_json_path = os.path.join(os.path.abspath(__file__ + "/../"), 'practice-automation-credentials.json')
token_json_path = os.path.join(os.path.abspath(__file__ + "/../"), 'token.json')


def create_message(sender, to, subject, html_content):
    message = MIMEText(html_content, "html")
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}


def send_mail(subject, html_body):
    creds = None
    if os.path.exists(token_json_path):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_json_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_json_path, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    message = create_message(
        sender="anshulbidhuri9876@gmail.com",
        to="anshulbidhuri9876@gmail.com",
        subject=subject,
        html_content=html_body
    )

    sent_message = service.users().messages().send(userId="me", body=message).execute()
    log.info(f"✅ Email sent! Message ID: {sent_message['id']}")
