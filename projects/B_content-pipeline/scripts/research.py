"""리서치 어시스턴트 — 주제를 주면 리서치 노트를 마크다운으로 만든다.

통계와 인용을 요구할 때는 **출처를 지어내지 말라고 명시**해야 한다.
그러지 않으면 그럴듯한 기관 이름이 붙은 가짜 수치가 나온다.
"""
import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from claude_call import ask

ROOT = Path(__file__).resolve().parent.parent

PROMPT = """다음 주제로 리서치 노트를 만들어 줘.

주제: {topic}
타겟 독자: {audience}

## 1. 현황 분석 — 관련 통계와 트렌드
## 2. 핵심 포인트 — 이 주제에서 꼭 다뤄야 할 5가지
## 3. 경쟁 분석 — 이미 나와 있는 콘텐츠와 우리의 차별점
## 4. 인용 및 참고
## 5. FAQ — 독자가 자주 묻는 질문 5개

{rule}

마크다운 본문만 출력해. 코드펜스로 감싸지 마.
"""

STRICT = """규칙 (반드시 지킬 것):
- **출처를 지어내지 마라.** 실제로 확인한 자료만 기관명·연도와 함께 적는다.
- 확인하지 못한 수치는 숫자를 쓰지 말고 "확인 필요"로 표시한다.
- 인물 인용도 마찬가지다. 실존 인물의 실제 발언만 적고, 아니면 넣지 않는다.
- 4번 항목에는 [확인함] / [확인 필요] 를 각 줄 앞에 붙인다."""

LOOSE = """관련 통계는 출처(기관, 연도)와 함께 적어 줘.
전문가 의견도 인용문 형태로 넣어 줘."""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topic', required=True)
    ap.add_argument('--audience', default='직장인')
    ap.add_argument('--slug', required=True)
    ap.add_argument('--loose', action='store_true',
                    help='출처 검증 규칙을 빼고 요청한다 (비교용)')
    a = ap.parse_args()

    md = ask(PROMPT.format(topic=a.topic, audience=a.audience,
                           rule=LOOSE if a.loose else STRICT))
    head = (f'# 리서치 노트: {a.topic}\n'
            f'**조사일:** {date.today()}\n'
            f'**조사자:** Claude Code (claude -p)\n\n---\n\n')
    name = f'{date.today()}_{a.slug}{"_loose" if a.loose else ""}.md'
    out = ROOT / 'content' / 'research' / name
    out.write_text(head + md + '\n', encoding='utf-8')
    print(f'📚 리서치 노트 작성 완료 ({len(md):,}자)')
    print(f'📁 {out.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
