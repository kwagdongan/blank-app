import streamlit as st
import pandas as pd
import numpy as np

st.subheader("리뷰 수 vs 긍정 비율 분석")

# 1. 데이터 로드 및 이상치 필터링
df = st.session_state['df']

# 리뷰 수가 너무 적은 데이터(예: 10개 미만)는 통계적 의미가 없으므로 제외
# 데이터 타입이 확실하게 숫자인지 재확인
df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
df['positive_percentual'] = pd.to_numeric(df['positive_percentual'], errors='coerce')

# 리뷰 수가 10개 이상인 게임만 대상으로 산점도 출력 (신뢰도 확보)
filtered_df = df[(df['total_reviews'] > 0) & (df['positive_percentual'] > 0)].copy()

# 2. 산점도 출력
top_reviews_df = filtered_df.nlargest(500, 'total_reviews')

px.scatter(
    top_reviews_df, 
    x='total_reviews', 
    y='positive_percentual',
    hover_name='name',  # 게임 이름 제목 표시
    hover_data={
        'total_reviews': ':,.0f',         # 콤마 찍고 정수형으로 표시
        'positive_percentual': ':.1f%',   # % 붙여서 소수점 첫째 자리까지 표시
        'name': False                     # hover_name으로 쓰이므로 리스트에서 제외
    },
    labels={
        'total_reviews': '총 리뷰 수',
        'positive_percentual': '긍정 평가 비율'
    },
    title='게임별 리뷰 수 vs 긍정 비율'
)

st.write(f"분석 중인 게임 수: {len(filtered_df)}개 (리뷰 10개 미만 제외)")
