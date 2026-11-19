"""책 13장 예제 데이터. 2025년 매출 1,234행 × 8열."""
import numpy as np, pandas as pd
rng = np.random.default_rng(20250101)

PRODUCTS = {
    '스마트워치 X1': ('웨어러블', 289000), '무선이어폰 A2': ('오디오', 159000),
    '블루투스 스피커 S3': ('오디오', 98000), '노트북 스탠드 D1': ('액세서리', 45000),
    '기계식 키보드 K7': ('액세서리', 132000), '4K 웹캠 W2': ('영상', 187000),
    '휴대용 SSD 1TB': ('저장장치', 142000), '고속 충전기 65W': ('액세서리', 39000),
    '모니터 27인치 QHD': ('디스플레이', 349000), '무선 마우스 M5': ('액세서리', 52000),
}
REGIONS = ['서울', '경기', '부산', '대구', '광주', '대전']
RW = np.array([0.31, 0.24, 0.13, 0.11, 0.11, 0.10])

n = 1234
days = pd.date_range('2025-01-01', '2025-12-31')
# 11~12월 시즌 효과: 하반기로 갈수록 판매가 몰린다
w = np.array([1.0 + 0.9 * (d.month >= 11) + 0.25 * (d.month in (5, 6)) for d in days])
dates = rng.choice(days, size=n, p=w / w.sum())

names = rng.choice(list(PRODUCTS), size=n,
                   p=np.array([.09,.14,.11,.09,.10,.07,.08,.13,.06,.13]))
rows = []
for d, name in zip(pd.to_datetime(sorted(dates)), names):
    cat, base = PRODUCTS[name]
    price = int(base * rng.uniform(0.9, 1.05) // 1000 * 1000)
    qty = int(rng.integers(1, 9))
    if d.month >= 11:
        qty += int(rng.integers(0, 4))
    rows.append({
        '날짜': d, '제품명': name, '카테고리': cat, '수량': qty,
        '단가': price, '매출액': price * qty,
        '지역': rng.choice(REGIONS, p=RW),
        # 마케팅비는 매출을 그대로 따라가지 않는다. 캠페인 단위로 흔들리게 둔다
        '마케팅비용': int(price * qty * 0.10 * rng.lognormal(0, 0.45)),
    })
df = pd.DataFrame(rows)

# 결측치를 일부러 섞는다 — 책이 결측치 처리 절을 다룬다
for col, k in (('수량', 7), ('지역', 5), ('마케팅비용', 11)):
    df.loc[rng.choice(df.index, k, replace=False), col] = np.nan

df.to_excel('data/sales_2025.xlsx', index=False)
df.to_csv('data/sales_2025.csv', index=False, encoding='utf-8-sig')
print(f'{len(df):,}행 × {df.shape[1]}열 저장')
print(df.head(3).to_string())
