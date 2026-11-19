"""CSV·Excel 파일을 불러오고 정제한다. 한글 인코딩과 결측치를 자동으로 처리한다."""
import sys

import pandas as pd

ENCODINGS = ('utf-8-sig', 'utf-8', 'cp949', 'euc-kr')


def load(path, sheet=0):
    """파일 형식을 보고 알맞게 읽는다. CSV 는 인코딩을 차례로 시도한다."""
    if str(path).lower().endswith(('.xlsx', '.xls')):
        df = pd.read_excel(path, sheet_name=sheet)
    else:
        for enc in ENCODINGS:
            try:
                df = pd.read_csv(path, encoding=enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise UnicodeDecodeError('지원하는 인코딩으로 읽지 못했습니다')
    for col in df.columns:
        if '날짜' in col or '일자' in col:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df


def clean(df):
    """결측치를 채운다. 숫자는 중앙값, 범주형은 최빈값 — 매출 데이터의 기본값이다."""
    out = df.copy()
    filled = {}
    for col in out.columns:
        n = int(out[col].isna().sum())
        if not n:
            continue
        if pd.api.types.is_numeric_dtype(out[col]):
            v = out[col].median()
            out[col] = out[col].fillna(v)
            filled[col] = (n, '중앙값', round(float(v), 1))
        else:
            v = out[col].mode().iloc[0]
            out[col] = out[col].fillna(v)
            filled[col] = (n, '최빈값', v)
    return out, filled


def summary(df):
    """컬럼별 타입·결측치·예시를 표로 만든다."""
    rows = []
    for col in df.columns:
        rows.append({
            '컬럼명': col,
            '타입': str(df[col].dtype),
            '결측치': int(df[col].isna().sum()),
            '예시': str(df[col].dropna().iloc[0])[:20] if df[col].notna().any() else '',
        })
    return pd.DataFrame(rows)


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'data/sales_2025.xlsx'
    df = load(path)
    print('데이터 로드 완료')
    print(f'  파일: {path.split("/")[-1]}')
    print(f'  크기: {len(df):,}행 × {df.shape[1]}열')
    print()
    print('컬럼 정보')
    print(summary(df).to_string(index=False))
    clean_df, filled = clean(df)
    if filled:
        print()
        print('결측치 처리')
        for col, (n, how, v) in filled.items():
            print(f'  {col}: {n}건 → {how} {v} 로 채움')
