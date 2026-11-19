"""아이디어 생성기 — 주제 영역과 타겟 독자를 주면 제목 후보를 뽑는다."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from claude_call import ask

ROOT = Path(__file__).resolve().parent.parent

PROMPT = """콘텐츠 아이디어를 만들어 줘.

주제 영역: {topic}
타겟 독자: {audience}
콘텐츠 유형: {ctype}

제목 후보 {count}개를 만들고, 각각을 다음 기준으로 1~5점 평가해 줘.
- 검색 수요: 사람들이 실제로 검색하는 주제인가
- 경쟁 강도: 이미 좋은 콘텐츠가 많은가 (낮을수록 좋음)
- 전문성 매치: 글쓴이 전문 분야와 맞는가
- 시의성: 지금 다룰 이유가 있는가

아래 JSON 배열만 출력해. 설명·코드펜스 없이 여는 대괄호부터 닫는 대괄호까지만.
[{{"title":"제목","search":4,"competition":2,"fit":5,"timing":4,"why":"한 줄 이유"}}]
"""


def extract_json(text):
    """모델 출력에서 가장 큰 JSON 배열을 뽑는다. 코드펜스와 군더더기를 견딘다."""
    best = None
    for i, ch in enumerate(text):
        if ch != '[':
            continue
        try:
            v, _ = json.JSONDecoder().raw_decode(text[i:])
        except ValueError:
            continue
        if isinstance(v, list) and (best is None or len(v) > len(best)):
            best = v
    if best is None:
        raise ValueError('JSON 배열을 찾지 못했습니다.\n' + text[:300])
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topic', required=True)
    ap.add_argument('--audience', required=True)
    ap.add_argument('--type', dest='ctype', default='실용')
    ap.add_argument('--count', type=int, default=10)
    a = ap.parse_args()

    ideas = extract_json(ask(PROMPT.format(topic=a.topic, audience=a.audience,
                                           ctype=a.ctype, count=a.count)))
    for x in ideas:
        x['score'] = x['search'] + (6 - x['competition']) + x['fit'] + x['timing']
    ideas.sort(key=lambda x: -x['score'])

    print('💡 콘텐츠 아이디어 생성 완료!')
    print(f'   {len(ideas)}개 · 주제 "{a.topic}" · 독자 "{a.audience}"')
    print()
    for i, x in enumerate(ideas, 1):
        mark = '🔥' if x['score'] >= 17 else '⭐' if x['score'] >= 14 else '  '
        print(f'{mark} {i:>2}. {x["title"]}')
        print(f'      점수 {x["score"]}/20 (수요 {x["search"]} · 경쟁 {x["competition"]}'
              f' · 적합 {x["fit"]} · 시의성 {x["timing"]})')
        print(f'      {x["why"]}')
    out = ROOT / 'content' / 'ideas.json'
    out.write_text(json.dumps(ideas, ensure_ascii=False, indent=2), encoding='utf-8')
    print()
    print(f'🏆 선택: "{ideas[0]["title"]}"')
    print(f'📁 저장: {out.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
