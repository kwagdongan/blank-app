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
filtered_df = df[df['total_reviews'] >= 30].copy()

# 2. 산점도 출력
st.scatter_chart(
    filtered_df,
    x='total_reviews',
    y='positive_percentual'
)

st.write(f"분석 중인 게임 수: {len(filtered_df)}개 (리뷰 10개 미만 제외)")
