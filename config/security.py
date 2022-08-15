import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from groo.groo import get_root
from sqlalchemy import select

from db import session
from db.model.token import Token

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/calendar.events.readonly',
          'https://www.googleapis.com/auth/calendar.events']


def getToken():
    creds = None

    token = session.execute(select(Token.token).where(Token.id == 'VitSen')).fetchone()

    if token is not None:
        creds = Credentials.from_authorized_user_info(json.loads(token[0]), scopes=SCOPES)
        return creds

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(get_root('credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)

        session.add(Token(id='VitSen', token=creds.to_json()))
        session.commit()
        return creds
