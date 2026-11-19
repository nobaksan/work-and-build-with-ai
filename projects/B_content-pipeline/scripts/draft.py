"""초안 생성기 — 리서치 노트를 넘겨 블로그 초안을 받는다."""
import argparse
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from claude_call import ask

ROOT = Path(__file__).resolve().parent.parent

PROMPT = """다음 리서치 노트를 바탕으로 블로그 글을 작성해 줘.

요구사항
- 길이: {length}
- 어조: 친근하지만 전문적, "~해요" 체
- 타겟 독자: AI 초보 직장인
- 구조: 도입(공감) → 단계별 방법 → 검토 → 마무리(행동 제안)
- 각 단계에 실제로 복사해 쓸 수 있는 프롬프트를 넣을 것
- 맨 위에 제목·메타 설명·태그를 붙일 것
- **리서치 노트에 없는 수치는 쓰지 말 것.** 노트의 수치를 쓸 때는 출처를 함께 적을 것
- 이미지가 들어갈 자리는 [IMAGE: 설명] 으로 표시

마크다운 본문만 출력해. 코드펜스로 감싸지 마.

--- 리서치 노트 ---
{note}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--note', required=True)
    ap.add_argument('--length', default='1800-2200자')
    ap.add_argument('--slug', required=True)
    a = ap.parse_args()

    note = Path(a.note).read_text(encoding='utf-8')
    md = ask(PROMPT.format(length=a.length, note=note))
    out = ROOT / 'content' / 'drafts' / f'{date.today()}_{a.slug}.md'
    out.write_text(md + '\n', encoding='utf-8')
    print(f'✍️  초안 작성 완료 ({len(md):,}자)')
    print(f'📁 {out.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
