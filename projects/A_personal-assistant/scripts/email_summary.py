"""Gmail 에서 중요 메일만 뽑아 한 줄씩 요약한다."""
import base64
import sys

from google_auth import NotConnected, service


def fetch(limit=5, query='is:unread -category:promotions -category:social'):
    svc = service('gmail', 'v1')
    res = svc.users().messages().list(userId='me', q=query, maxResults=limit).execute()
    out = []
    for m in res.get('messages', []):
        msg = svc.users().messages().get(userId='me', id=m['id'],
                                         format='metadata',
                                         metadataHeaders=['From', 'Subject']).execute()
        h = {x['name']: x['value'] for x in msg['payload']['headers']}
        out.append({'from': h.get('From', '')[:30],
                    'subject': h.get('Subject', '(제목 없음)'),
                    'snippet': msg.get('snippet', '')[:60]})
    return out


def lines(limit=5):
    try:
        mails = fetch(limit)
    except NotConnected as e:
        first, *rest = str(e).split('\n')
        return [f'  (연동 안 됨) {first}'] + [f'  {r.strip()}' for r in rest]
    if not mails:
        return ['  읽지 않은 중요 메일이 없습니다.']
    return [f'  · {m["subject"]}  — {m["from"]}' for m in mails]


if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print('중요 메일')
    for l in lines(n):
        print(l)
