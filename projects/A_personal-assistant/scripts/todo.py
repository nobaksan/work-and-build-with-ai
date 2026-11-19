#!/usr/bin/env python3
"""할 일 관리 — 외부 API 없이 JSON 파일 하나로 돌아간다.

  python scripts/todo.py add "보고서 작성" --priority high --due tomorrow
  python scripts/todo.py list [--today] [--priority high] [--all]
  python scripts/todo.py done 1
  python scripts/todo.py stats
"""
import argparse
import json
import os
import unicodedata
from datetime import date, datetime, timedelta
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / 'data' / 'todos.json'


def today():
    """오늘 날짜. 책의 예시 화면을 다시 뽑을 때는 TODO_TODAY 로 고정한다."""
    v = os.environ.get('TODO_TODAY')
    return date.fromisoformat(v) if v else date.today()

PRIORITY = {'high': '높음', 'medium': '보통', 'low': '낮음'}
WEEKDAY = '월화수목금토일'
REPEAT = {'daily': '매일', 'weekly': '매주', 'monthly': '매월'}


def load():
    if not DATA.exists():
        return []
    return json.loads(DATA.read_text(encoding='utf-8'))


def save(items):
    DATA.parent.mkdir(exist_ok=True)
    DATA.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')


def parse_due(s):
    """오늘/내일/모레 같은 말도 날짜로 받아 준다."""
    if not s:
        return None
    base = today()
    words = {'today': 0, '오늘': 0, 'tomorrow': 1, '내일': 1, '모레': 2}
    if s in words:
        return (base + timedelta(days=words[s])).isoformat()
    try:
        return datetime.strptime(s, '%Y-%m-%d').date().isoformat()
    except ValueError:
        raise SystemExit(f'날짜를 알아듣지 못했습니다: {s}\n'
                         '  예) --due tomorrow  --due 2026-09-01')


def fmt_due(v):
    if not v:
        return '없음'
    d = date.fromisoformat(v)
    delta = (d - today()).days
    tag = {0: ' (오늘)', 1: ' (내일)'}.get(delta, f' (D{delta:+d})' if delta else '')
    return f'{v} ({WEEKDAY[d.weekday()]}){tag}'


def add(args):
    items = load()
    item = {'id': max([i['id'] for i in items], default=0) + 1,
            'text': args.text, 'priority': args.priority,
            'due': parse_due(args.due), 'tag': args.tag,
            'repeat': args.repeat, 'done': False,
            'created': datetime.now().isoformat(timespec='seconds')}
    items.append(item)
    save(items)
    head = '반복 할 일을 추가했습니다.' if item['repeat'] else '할 일을 추가했습니다.'
    print(head)
    print(f'  [{item["id"]}] {item["text"]}')
    print(f'  우선순위 {PRIORITY[item["priority"]]}  ·  마감 {fmt_due(item["due"])}')
    if item['tag']:
        print(f'  태그 #{item["tag"]}')
    if item['repeat']:
        print(f'  반복 {REPEAT[item["repeat"]]}')


def pad(s, width):
    """한글은 두 칸을 차지한다. 터미널에서 열을 맞추려면 글자 수가 아니라 폭으로 센다."""
    w = sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in s)
    return s + ' ' * max(0, width - w)


def _rows(items):
    order = {'high': 0, 'medium': 1, 'low': 2}
    return sorted(items, key=lambda i: (order[i['priority']], i['due'] or '9999'))


def show(args):
    items = load()
    if not args.all:
        items = [i for i in items if not i['done']]
    if args.today:
        items = [i for i in items if i['due'] == today().isoformat()]
    if args.priority:
        items = [i for i in items if i['priority'] == args.priority]
    day = today()
    title = (f'오늘의 할 일 ({day} {WEEKDAY[day.weekday()]}요일)'
             if args.today else '전체 할 일 목록' if args.all else '할 일 목록')
    print(title)
    print('-' * 56)
    if not items:
        print('  비어 있습니다. add 로 추가하세요.')
        return
    for i in _rows(items):
        mark = 'x' if i['done'] else ' '
        due = f'  마감 {i["due"]}' if i['due'] else ''
        tag = f'  #{i["tag"]}' if i['tag'] else ''
        print(f'  [{mark}] {i["id"]:>2}. {pad(i["text"], 30)} {PRIORITY[i["priority"]]}{due}{tag}')
    print('-' * 56)
    done = sum(1 for i in load() if i['done'])
    total = len(load())
    print(f'  총 {total}건 · 완료 {done}건 · 남음 {total - done}건')


def done(args):
    items = load()
    for i in items:
        if i['id'] == args.id:
            if i['done']:
                print(f'  [{i["id"]}] {i["text"]} — 이미 완료된 항목입니다.')
                return
            i['done'] = True
            i['completed'] = f"{today()}T{datetime.now():%H:%M:%S}"
            save(items)
            total = len(items)
            fin = sum(1 for x in items if x['done'])
            today_fin = sum(1 for x in items if x.get('completed', '')
                            .startswith(today().isoformat()))
            print('완료했습니다.')
            print(f'  [{i["id"]}] {i["text"]}')
            print(f'  오늘 완료 {today_fin}건  ·  '
                  f'전체 완료율 {fin / total * 100:.1f}% ({fin}/{total})')
            return
    raise SystemExit(f'ID {args.id} 인 할 일을 찾지 못했습니다. list 로 확인하세요.')


def stats(args):
    items = load()
    if not items:
        print('할 일이 없습니다.')
        return
    fin = sum(1 for i in items if i['done'])
    print('할 일 통계')
    print(f'  전체 {len(items)}건 · 완료 {fin}건 · 완료율 {fin / len(items) * 100:.1f}%')
    for key, label in PRIORITY.items():
        n = sum(1 for i in items if i['priority'] == key)
        if n:
            done_n = sum(1 for i in items if i['priority'] == key and i['done'])
            print(f'  {label} {n}건 (완료 {done_n})')


def main():
    ap = argparse.ArgumentParser(description='할 일 관리')
    sub = ap.add_subparsers(dest='cmd', required=True)

    a = sub.add_parser('add', help='할 일 추가')
    a.add_argument('text')
    a.add_argument('--priority', choices=list(PRIORITY), default='medium')
    a.add_argument('--due')
    a.add_argument('--tag')
    a.add_argument('--repeat', choices=['daily', 'weekly', 'monthly'])
    a.set_defaults(func=add)

    l = sub.add_parser('list', help='할 일 보기')
    l.add_argument('--today', action='store_true')
    l.add_argument('--all', action='store_true')
    l.add_argument('--priority', choices=list(PRIORITY))
    l.set_defaults(func=show)

    d = sub.add_parser('done', help='완료 처리')
    d.add_argument('id', type=int)
    d.set_defaults(func=done)

    s = sub.add_parser('stats', help='통계')
    s.set_defaults(func=stats)

    args = ap.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
