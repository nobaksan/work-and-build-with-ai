"""Google Calendar 에서 일정을 가져온다."""
import sys
from datetime import datetime, timedelta, timezone

from google_auth import NotConnected, service

KST = timezone(timedelta(hours=9))


def fetch(days=1):
    svc = service('calendar', 'v3')
    now = datetime.now(KST)
    end = (now + timedelta(days=days)).replace(hour=23, minute=59)
    res = svc.events().list(calendarId='primary', timeMin=now.isoformat(),
                            timeMax=end.isoformat(), singleEvents=True,
                            orderBy='startTime', maxResults=20).execute()
    out = []
    for e in res.get('items', []):
        s = e['start'].get('dateTime', e['start'].get('date'))
        out.append({'time': s[11:16] if 'T' in s else '종일',
                    'title': e.get('summary', '(제목 없음)'),
                    'where': e.get('location', ''),
                    'attendees': len(e.get('attendees', []))})
    return out


def lines(days=1):
    try:
        events = fetch(days)
    except NotConnected as e:
        first, *rest = str(e).split('\n')
        return [f'  (연동 안 됨) {first}'] + [f'  {r.strip()}' for r in rest]
    if not events:
        return ['  일정이 없습니다. 좋은 날입니다.']
    return [f'  {e["time"]}  {e["title"]}'
            + (f'  @{e["where"]}' if e['where'] else '')
            + (f'  ({e["attendees"]}명)' if e['attendees'] else '')
            for e in events]


if __name__ == '__main__':
    days = 7 if 'week' in sys.argv else 1
    print(f'{"이번 주" if days > 1 else "오늘"} 일정')
    for l in lines(days):
        print(l)
