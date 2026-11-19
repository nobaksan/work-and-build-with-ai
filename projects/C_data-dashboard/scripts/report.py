"""분석·차트·인사이트를 하나의 리포트로 묶는다. 마크다운과 HTML 로 낸다."""
import json
import sys
from datetime import date

import insight

CHARTS = [('monthly_trend', '월별 매출 추이'), ('category_pie', '카테고리별 매출 비중'),
          ('region_bar', '지역별 매출'), ('correlation_heatmap', '상관관계 히트맵'),
          ('sales_histogram', '거래 건당 매출액 분포')]


def markdown(r, made_on):
    b, t = r['기본'], r['트렌드']
    md = [f'# 월간 매출 분석 리포트', '',
          f'**기간:** 2025년 1월 1일 ~ 2025년 12월 31일  ',
          f'**생성일:** {made_on}  ',
          f'**데이터:** sales_2025.xlsx ({b["건수"]:,}행)', '', '---', '',
          '## 1. 한 장 요약', '',
          f'2025년 매출은 총 {b["총매출"]:,}원이었습니다. 하반기가 상반기보다'f' {t["하반기증가율"]:.0f}% 많았고, {t["최고월"]}월 한 달에'f' {t["최고월매출"]/b["총매출"]*100:.0f}%가 몰렸습니다.', '',
          '## 2. 핵심 지표', '',
          '| 지표 | 값 |', '|---|---:|',
          f'| 총 매출 | {b["총매출"]:,}원 |',
          f'| 월 평균 | {b["월평균"]:,}원 |',
          f'| 거래 건수 | {b["건수"]:,}건 |',
          f'| 건당 평균 | {b["건당평균"]:,}원 |',
          f'| 최고 매출 월 | {t["최고월"]}월 ({t["최고월매출"]:,}원) |',
          f'| 최저 매출 월 | {t["최저월"]}월 ({t["최저월매출"]:,}원) |', '',
          '## 3. 차트', '']
    for name, title in CHARTS:
        md += [f'### {title}', '', f'![{title}](charts/{name}.png)', '']
    md += ['## 4. AI 인사이트', '', insight.report(r), '', '## 5. 부록 — 상세 데이터', '',
           '| 카테고리 | 매출액 |', '|---|---:|']
    md += [f'| {k} | {v:,} |' for k, v in r['카테고리'].items()]
    md += ['', '| 지역 | 매출액 |', '|---|---:|']
    md += [f'| {k} | {v:,} |' for k, v in r['지역'].items()]
    return '\n'.join(md)


def html(md_text):
    body = md_text.replace('&', '&amp;').replace('<', '&lt;')
    return ('<!doctype html><meta charset="utf-8"><title>월간 매출 분석 리포트</title>''<style>body{max-width:820px;margin:40px auto;padding:0 20px;''font-family:-apple-system,"Apple SD Gothic Neo",sans-serif;line-height:1.7;''color:#1b1f2a}pre{white-space:pre-wrap}</style>'f'<pre>{body}</pre>')


if __name__ == '__main__':
    r = json.load(open('output/analysis.json', encoding='utf-8'))
    made_on = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
    md = markdown(r, made_on)
    open('output/report.md', 'w', encoding='utf-8').write(md)
    open('output/report.html', 'w', encoding='utf-8').write(html(md))
    print('리포트 생성 완료')
    print('output/report.md')
    print('output/report.html')
    print(f'({len(md):,}자, 차트 {len(CHARTS)}개 포함)')
