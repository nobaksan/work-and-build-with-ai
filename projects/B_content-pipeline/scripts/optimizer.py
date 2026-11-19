"""원소스 멀티유즈 — 블로그 글 하나를 플랫폼별로 변환한다."""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from claude_call import ask

ROOT = Path(__file__).resolve().parent.parent

RULES = {
    'linkedin': '1,300자 이내. 첫 줄에 스크롤을 멈추게 하는 후킹. 개인 경험으로 시작. '
                '핵심은 숫자 목록. 문단은 1~2줄. 마지막에 질문형 CTA.',
    'twitter': '7개 트윗 쓰레드. 각 280자 이내. 1번은 후킹 + "↓". '
               '한 트윗에 한 가지만. 마지막은 요약과 CTA.',
    'instagram': '10장 캐러셀. 슬라이드마다 한 메시지. 슬라이드당 40자 이내. '
                 '1장 타이틀, 2장 공감, 3~8장 팁, 9장 요약, 10장 CTA.',
    'newsletter': '600~800자. 호기심을 부르는 제목. 인사말로 시작. 개인적인 이야기 포함. '
                  '"더 자세히는 블로그에서" 로 마무리.',
}

CHECK = {
    'twitter': ('트윗을 "1/7" 형태로 번호 매기고 "---" 로 구분',
                lambda s: len([b for b in s.split('---') if b.strip()]) == 7
                          and '1/7' in s),
    'linkedin': ('1,300자 이내', lambda s: len(s) <= 1300),
    'instagram': ('슬라이드 10장', lambda s: s.count('[슬라이드') == 10),
    'newsletter': ('600~800자', lambda s: 500 <= len(s) <= 900),
}

PROMPT = """다음 블로그 글을 {name} 용으로 변환해 줘.

규칙: {rule}
- **원문에 없는 수치나 주장을 새로 만들지 마라.**
- 결과 본문만 출력해. 설명도 코드펜스도 붙이지 마.

--- 원문 ---
{body}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--draft', required=True)
    ap.add_argument('--platforms', default='linkedin,twitter,instagram,newsletter')
    a = ap.parse_args()

    cfg = json.loads((ROOT / 'config' / 'platforms.json').read_text(encoding='utf-8'))
    body = Path(a.draft).read_text(encoding='utf-8')
    outdir = ROOT / 'output' / 'platforms' / str(date.today())
    outdir.mkdir(parents=True, exist_ok=True)

    print('🔄 플랫폼 최적화')
    for key in a.platforms.split(','):
        name = cfg.get(key, {}).get('name', key)
        desc, ok = CHECK[key]
        text = ask(PROMPT.format(name=name, rule=RULES[key], body=body))
        # 형식 제약은 프롬프트에 쓰는 것만으로 지켜지지 않는다. 한 번 더 시킨다.
        tries = 1
        while not ok(text) and tries < 3:
            tries += 1
            text = ask(f'아래 결과가 형식을 지키지 않았어. 조건: {desc}\n'
                       f'같은 내용으로 형식만 맞춰서 다시 써 줘. 본문만 출력해.\n\n{text}')
        (outdir / f'{key}.md').write_text(text + '\n', encoding='utf-8')
        mark = '✅' if ok(text) else '⚠️'
        note = '' if tries == 1 else f' (형식 교정 {tries - 1}회)'
        print(f'   {mark} {name}: {len(text):,}자{note}')
        if not ok(text):
            print(f'      형식 미충족 — 조건: {desc}. 직접 손봐야 합니다')
    print(f'📁 {outdir.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
