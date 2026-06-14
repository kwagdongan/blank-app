import streamlit as st
import pandas as pd
import ast


st.title("장르별 게임 분포 분석")

# 1. 데이터 로드 및 정제
df = st.session_state['df']

# 2. 데이터 펼치기
df_genres = df.explode('genres')

# 3. 빈도 분석
genre_counts = df_genres['genres'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']
genre_counts = genre_counts[genre_counts['Genre'] != '']

# 25% 경계값 (3사분위수)
q75 = genre_counts['Count'].quantile(0.85)

# 상위 25% 태그만 선택
top_quartile = genre_counts[genre_counts['Count'] >= q75]

st.subheader("태그 빈도 상위 25% (1분위 그룹)")

st.dataframe(top_quartile, use_container_width=True)

st.bar_chart(top_quartile.set_index('Genre'))
