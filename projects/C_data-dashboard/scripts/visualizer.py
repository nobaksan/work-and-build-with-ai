"""분석 결과를 다섯 가지 차트로 그린다. 회사 브랜드 색상과 한글 폰트를 적용한다."""
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt          # noqa: E402

from data_loader import clean, load      # noqa: E402

BLUE, GREEN = '#2563EB', '#10B981'
PALETTE = [BLUE, GREEN, '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#EC4899']

plt.rcParams['font.family'] = 'AppleGothic'      # macOS 한글 폰트
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 460                 # 인쇄용 — 가로 2,040px 이상
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.25


def _save(fig, name):
    path = f'output/charts/{name}.png'
    fig.savefig(path, facecolor='white')
    plt.close(fig)
    return path


def draw_all(df):
    df, _ = clean(df)
    made = []

    m = df.groupby(df['날짜'].dt.month)['매출액'].sum() / 1e6
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(m.index, m.values, marker='o', color=BLUE, linewidth=2.5)
    ax.fill_between(m.index, m.values, alpha=0.12, color=BLUE)
    ax.set_title('월별 매출 추이 (2025년)', fontsize=15)
    ax.set_xlabel('월')
    ax.set_ylabel('매출액 (백만원)')
    ax.set_xticks(range(1, 13))
    made.append(_save(fig, 'monthly_trend'))

    c = df.groupby('카테고리')['매출액'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.pie(c.values, labels=c.index, autopct='%1.1f%%', startangle=90,
           colors=PALETTE, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    ax.set_title('카테고리별 매출 비중', fontsize=15)
    made.append(_save(fig, 'category_pie'))

    r = df.groupby('지역')['매출액'].sum().sort_values() / 1e6
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(r.index, r.values, color=GREEN)
    for i, v in enumerate(r.values):
        ax.text(v, i, f' {v:.0f}', va='center', fontsize=10)
    ax.set_title('지역별 매출', fontsize=15)
    ax.set_xlabel('매출액 (백만원)')
    made.append(_save(fig, 'region_bar'))

    num = df[['수량', '단가', '매출액', '마케팅비용']].corr()
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    im = ax.imshow(num, cmap='RdBu_r', vmin=-1, vmax=1)
    ax.set_xticks(range(len(num)), num.columns, rotation=30, ha='right')
    ax.set_yticks(range(len(num)), num.columns)
    for i in range(len(num)):
        for j in range(len(num)):
            ax.text(j, i, f'{num.iloc[i, j]:.2f}', ha='center', va='center',
                    color='white' if abs(num.iloc[i, j]) > 0.5 else '#1b1f2a')
    ax.set_title('상관관계 히트맵', fontsize=15)
    ax.grid(False)
    fig.colorbar(im, ax=ax, shrink=0.8)
    made.append(_save(fig, 'correlation_heatmap'))

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(df['매출액'] / 1e4, bins=40, color=BLUE, alpha=0.85)
    ax.set_title('거래 건당 매출액 분포', fontsize=15)
    ax.set_xlabel('매출액 (만원)')
    ax.set_ylabel('건수')
    made.append(_save(fig, 'sales_histogram'))
    return made


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'data/sales_2025.xlsx'
    paths = draw_all(load(path))
    print('차트 생성 완료')
    print(f'  {len(paths)}개')
    for p in paths:
        print(f'  {p}')
