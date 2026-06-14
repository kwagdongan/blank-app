import streamlit as st
import pandas as pd
import ast


st.title("장르별 게임 분포 분석")

# 1. 데이터 로드 및 정제
df = st.session_state['df']

# 2. 데이터 펼치기
df_genres = df.explode('genres_list')

# 3. 빈도 분석
genre_counts = df_genres['genres_list'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']
genre_counts = genre_counts[genre_counts['Genre'] != ''] # 빈 값 제거

# 4. 결과 출력
st.subheader("장르별 게임 수 Top 5")
st.dataframe(genre_counts.head(5), use_container_width=True)

# 5. 시각화
st.bar_chart(genre_counts.head(5).set_index('Genre'))




