import streamlit as st
import pandas as pd
import numpy as np


st.subheader("리뷰 수 vs 긍정 비율 분석")


# 1. 데이터 로드 및 정제
df = st.session_state['df']

# 데이터 타입이 확실하게 숫자인지 재확인
df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
df['positive_percentual'] = pd.to_numeric(df['positive_percentual'], errors='coerce')



# 2. 산점도 출력
top_reviews_df = df.nlargest(500, 'total_reviews')

st.scatter_chart(
    df,
    x='total_reviews',
    y='positive_percentual'
)

st.write(f"분석 중인 게임 수: {len(filtered_df)}개 ")
