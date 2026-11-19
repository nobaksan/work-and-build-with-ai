"""데이터 분석 대시보드 — Streamlit.

실행: streamlit run app.py   (브라우저에서 http://localhost:8501 이 열린다)
"""
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent / 'scripts'))
from analyzer import analyze          # noqa: E402
from data_loader import clean, load, summary   # noqa: E402
import insight                        # noqa: E402

BLUE, GREEN = '#2563EB', '#10B981'
PALETTE = [BLUE, GREEN, '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#EC4899']

st.set_page_config(page_title='매출 분석 대시보드', layout='wide')


@st.cache_data
def read(path_or_buf, name):
    df = load(path_or_buf) if not hasattr(path_or_buf, 'read') else (
        pd.read_excel(path_or_buf) if name.endswith(('.xlsx', '.xls'))
        else pd.read_csv(path_or_buf))
    if '날짜' in df.columns:
        df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    return clean(df)[0]


with st.sidebar:
    st.header('데이터')
    up = st.file_uploader('CSV 또는 Excel 파일', type=['csv', 'xlsx', 'xls'])
    if up is None:
        st.caption('파일을 올리지 않으면 예제 데이터(sales_2025.xlsx)를 씁니다.')
        df = read('data/sales_2025.xlsx', 'sales_2025.xlsx')
        source = 'sales_2025.xlsx (예제)'
    else:
        df = read(up, up.name)
        source = up.name
    st.success(f'{len(df):,}행 × {df.shape[1]}열')

    st.header('필터')
    months = st.slider('기간 (월)', 1, 12, (1, 12))
    cats = st.multiselect('카테고리', sorted(df['카테고리'].unique()),
                          default=sorted(df['카테고리'].unique()))
    regions = st.multiselect('지역', sorted(df['지역'].unique()),
                             default=sorted(df['지역'].unique()))

f = df[df['날짜'].dt.month.between(*months)
       & df['카테고리'].isin(cats) & df['지역'].isin(regions)]

st.title('매출 분석 대시보드')
st.caption(f'{source} · {months[0]}월~{months[1]}월 · {len(f):,}건')

if f.empty:
    st.warning('조건에 맞는 데이터가 없습니다. 필터를 넓혀 보세요.')
    st.stop()

r = analyze(f)
b, t = r['기본'], r['트렌드']
c1, c2, c3, c4 = st.columns(4)
c1.metric('총 매출', f'{b["총매출"]/1e8:.2f}억 원')
c2.metric('거래 건수', f'{b["건수"]:,}건')
c3.metric('건당 평균', f'{b["건당평균"]:,}원')
c4.metric('최고 매출 월', f'{t["최고월"]}월',
          f'{t["최고월매출"]/1e8:.2f}억 원')

tabs = st.tabs(['차트', 'AI 인사이트', '데이터', '비교'])

with tabs[0]:
    m = f.groupby(f['날짜'].dt.month)['매출액'].sum().reset_index()
    m.columns = ['월', '매출액']
    st.plotly_chart(px.line(m, x='월', y='매출액', markers=True,
                            title='월별 매출 추이',
                            color_discrete_sequence=[BLUE]),
                    use_container_width=True)
    left, right = st.columns(2)
    cat = f.groupby('카테고리')['매출액'].sum().reset_index()
    left.plotly_chart(px.pie(cat, names='카테고리', values='매출액', hole=0.35,
                             title='카테고리별 비중',
                             color_discrete_sequence=PALETTE),
                      use_container_width=True)
    reg = f.groupby('지역')['매출액'].sum().sort_values().reset_index()
    right.plotly_chart(px.bar(reg, x='매출액', y='지역', orientation='h',
                              title='지역별 매출',
                              color_discrete_sequence=[GREEN]),
                       use_container_width=True)

with tabs[1]:
    st.markdown(insight.report(r).replace('\n', '  \n'))
    with st.expander('Claude에게 그대로 물어볼 프롬프트'):
        st.code(insight.PROMPT.format(facts=insight.facts(r)), language='text')

with tabs[2]:
    st.dataframe(summary(f), use_container_width=True, hide_index=True)
    st.dataframe(f, use_container_width=True, hide_index=True, height=320)
    st.download_button('엑셀로 내려받기', f.to_csv(index=False).encode('utf-8-sig'),
                       'filtered.csv', 'text/csv')

with tabs[3]:
    half = f.assign(반기=f['날짜'].dt.month.map(lambda x: '상반기' if x <= 6 else '하반기'))
    piv = half.pivot_table(index='카테고리', columns='반기', values='매출액',
                           aggfunc='sum', fill_value=0)
    if {'상반기', '하반기'} <= set(piv.columns):
        piv['증감률(%)'] = ((piv['하반기'] / piv['상반기'].replace(0, pd.NA) - 1)
                         * 100).round(1)
    st.dataframe(piv, use_container_width=True)
