#!/usr/bin/env python3
"""데일리 브리핑 — 일정·메일·할 일을 한 화면에 모은다.

연동되지 않은 항목은 건너뛰지 않고 "연동 안 됨"으로 표시한다.
무엇이 빠졌는지 보이지 않으면 브리핑을 믿을 수 없다.
"""
import json
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import calendar_sync
import email_summary
import todo

ROOT = Path(__file__).resolve().parent.parent
WEEKDAY = '월화수목금토일'
W = 60


def rule(ch='-'):
    return ch * W


def weather(cfg):
    """날씨. API 키가 없으면 그렇게 적는다."""
    key = cfg.get('weather', {}).get('api_key')
    if not key or key.startswith('your-'):
        return '(연동 안 됨) config/settings.json 의 weather.api_key 를 넣으세요'
    import requests
    city = cfg['weather'].get('city', 'Seoul')
    r = requests.get('https://api.openweathermap.org/data/2.5/weather',
                     params={'q': city, 'appid': key, 'units': 'metric', 'lang': 'kr'},
                     timeout=5)
    d = r.json()
    return (f'{d["weather"][0]["description"]} {d["main"]["temp"]:.0f}°C '
            f'(체감 {d["main"]["feels_like"]:.0f}°C)')


def todo_lines():
    items = [i for i in todo.load() if not i['done']]
    today = todo.today().isoformat()
    due_today = [i for i in items if i['due'] == today]
    high = [i for i in items if i['priority'] == 'high' and i not in due_today]
    if not items:
        return ['  남은 할 일이 없습니다.']
    out = []
    for i in due_today:
        out.append(f'  오늘 마감      {i["text"]}')
    for i in high:
        out.append(f'  우선순위 높음  {i["text"]}')
    rest = len(items) - len(due_today) - len(high)
    if rest > 0:
        out.append(f'  … 그 밖에 {rest}건')
    return out


def main():
    cfg = json.loads((ROOT / 'config' / 'settings.json').read_text(encoding='utf-8'))
    name = cfg['user']['name']
    today = todo.today()
    print(rule('='))
    print(f'  {name} 님의 데일리 브리핑')
    print(f'  {today.year}년 {today.month}월 {today.day}일 '
          f'({WEEKDAY[today.weekday()]})')
    print(rule('='))
    print()
    print('날씨')
    print(f'  {weather(cfg)}')
    print()
    print('오늘 일정')
    for l in calendar_sync.lines(1):
        print(l)
    print()
    print('중요 메일')
    for l in email_summary.lines(5):
        print(l)
    print()
    print('할 일')
    for l in todo_lines():
        print(l)
    print()
    print(rule())
    items = todo.load()
    done_n = sum(1 for i in items if i['done'])
    print(f'  할 일 {len(items)}건 중 {done_n}건 완료. 좋은 하루 보내세요.')
    print(rule())


if __name__ == '__main__':
    main()
