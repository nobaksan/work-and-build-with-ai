"""Google API 인증. 자격 증명이 없으면 예외 대신 사유를 돌려준다.

책의 독자 대부분은 이 절을 읽는 시점에 credentials.json 이 없다.
그때 프로그램이 죽어 버리면 다음 절로 나아갈 수 없으므로, 없으면 없다고 말하고
나머지 기능은 그대로 돌아가게 만든다.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CRED_DIR = ROOT / 'config' / 'credentials'
CRED = CRED_DIR / 'credentials.json'

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly',
          'https://www.googleapis.com/auth/gmail.readonly']


class NotConnected(Exception):
    """연동이 아직 안 된 상태. 오류가 아니라 '아직'이다."""


def service(name, version):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    if not CRED.exists():
        raise NotConnected(
            'config/credentials/credentials.json 이 없습니다.\n'
            '     Google Cloud Console에서 OAuth 클라이언트 ID(데스크톱 앱)를 만들어\n'
            '     내려받은 파일을 config/credentials/credentials.json 으로 저장하세요.')
    CRED_DIR.mkdir(exist_ok=True)
    token = CRED_DIR / 'token.json'
    creds = Credentials.from_authorized_user_file(token, SCOPES) if token.exists() else None
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(CRED), SCOPES)
        creds = flow.run_local_server(port=0)
        token.write_text(creds.to_json(), encoding='utf-8')
    return build(name, version, credentials=creds)
