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

df = df[(df['total_reviews'] > 30) & (df['positive_percentual'] > 0)].copy()

# 리뷰 수에 로그 변환 적용 (리뷰 1개 = 0, 100개 = 2, 10000개 = 4 등)
df['log_reviews'] = np.log10(df['total_reviews'])

# 이제 log_reviews를 x축으로 사용
st.scatter_chart(
    df, 
    x='log_reviews', 
    y='positive_percentual'
)
st.write(f"분석 중인 게임 수: {len(filtered_df)}개 (리뷰 30개 미만 제외)")
