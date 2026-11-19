"""매출 데이터를 자동으로 분석한다. 기술 통계·트렌드·상관관계·이상치·그룹 비교."""
import json
import sys
import unicodedata

from data_loader import clean, load


def analyze(df):
    df, _ = clean(df)
    r = {}
    s = df['매출액']
    r['기본'] = {
        '총매출': int(s.sum()),
        '월평균': int(s.sum() / df['날짜'].dt.month.nunique()),
        '건수': int(len(df)),
        '건당평균': int(s.mean()),
        '중앙값': int(s.median()),
        '표준편차': int(s.std()),
        '최대': int(s.max()),
        '최소': int(s.min()),
    }
    m = df.groupby(df['날짜'].dt.month)['매출액'].sum()
    r['월별'] = {int(k): int(v) for k, v in m.items()}
    r['트렌드'] = {
        '최고월': int(m.idxmax()), '최고월매출': int(m.max()),
        '최저월': int(m.idxmin()), '최저월매출': int(m.min()),
        '상반기': int(m[m.index <= 6].sum()),
        '하반기': int(m[m.index > 6].sum()),
    }
    r['트렌드']['하반기증가율'] = round(
        (r['트렌드']['하반기'] / r['트렌드']['상반기'] - 1) * 100, 1)

    for key, col in (('카테고리', '카테고리'), ('지역', '지역'), ('제품', '제품명')):
        g = df.groupby(col)['매출액'].sum().sort_values(ascending=False)
        r[key] = {k: int(v) for k, v in g.items()}

    num = df[['수량', '단가', '매출액', '마케팅비용']]
    r['상관관계'] = {f'{a}-{b}': round(float(num[a].corr(num[b])), 2)
                  for i, a in enumerate(num.columns) for b in num.columns[i + 1:]}

    q1, q3 = s.quantile([.25, .75])
    hi = s > q3 + 1.5 * (q3 - q1)
    r['이상치'] = {
        '건수': int(hi.sum()), '기준': int(q3 + 1.5 * (q3 - q1)),
        '합계': int(s[hi].sum()),
        '비중': round(float(s[hi].sum() / s.sum() * 100), 1),
    }
    return r


def pad(s, width):
    """한글은 두 칸을 차지한다. 열을 맞추려면 글자 수가 아니라 폭으로 센다."""
    w = sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in s)
    return s + ' ' * max(0, width - w)


def report(r):
    b, t = r['기본'], r['트렌드']
    top_cat = next(iter(r['카테고리']))
    top_reg = next(iter(r['지역']))
    out = [
        '분석 완료', '',
        '매출',
        f'  총 매출      {b["총매출"]:>15,} 원',
        f'  월 평균      {b["월평균"]:>15,} 원',
        f'  거래 건수    {b["건수"]:>15,} 건  (건당 평균 {b["건당평균"]:,} 원)',
        f'  최고 매출 월 {t["최고월"]:>13} 월  ({t["최고월매출"]:,} 원)',
        f'  최저 매출 월 {t["최저월"]:>13} 월  ({t["최저월매출"]:,} 원)', '',
        '구성',
        f'  1위 카테고리  {pad(top_cat, 10)}{r["카테고리"][top_cat]:>13,} 원'
        f'  ({r["카테고리"][top_cat] / b["총매출"] * 100:.1f}%)',
        f'  1위 지역      {pad(top_reg, 10)}{r["지역"][top_reg]:>13,} 원'
        f'  ({r["지역"][top_reg] / b["총매출"] * 100:.1f}%)', '',
        '트렌드',
        f'  상반기 {t["상반기"]:,} 원  →  하반기 {t["하반기"]:,} 원'
        f'  ({t["하반기증가율"]:+.1f}%)', '',
        '상관관계',
    ]
    for k, v in sorted(r['상관관계'].items(), key=lambda x: -abs(x[1]))[:3]:
        out.append(f'  {pad(k.replace("-", " - "), 24)}{v}')
    out += ['', '이상치',
            f'  {r["이상치"]["건수"]}건이 {r["이상치"]["기준"]:,} 원을 넘습니다'
            f'  (매출의 {r["이상치"]["비중"]}%)']
    return '\n'.join(out)


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'data/sales_2025.xlsx'
    r = analyze(load(path))
    print(report(r))
    with open('output/analysis.json', 'w', encoding='utf-8') as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
    print()
    print('→ output/analysis.json 저장')
