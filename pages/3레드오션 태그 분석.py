import streamlit as st
import pandas as pd
import ast

st.title("태그별 게임 분포 분석")

# 1. 데이터 로드
df = st.session_state['df']

# 2. 데이터 펼치기
df_genres = df.explode('genres')

# 3. 빈도 분석
genre_counts = df_genres['genres'].value_counts().reset_index()
genre_counts.columns = ['태그', '빈도']
genre_counts = genre_counts[genre_counts['태그'] != '']

# 상위 8% 기준 (현재 코드 기준)
q75 = genre_counts['빈도'].quantile(0.92)

top_quartile = genre_counts[genre_counts['빈도'] >= q75]

# 평균 빈도 계산
avg_count = top_quartile['빈도'].mean()

st.subheader("태그 빈도 상위 그룹")

# 평균 빈도 표시
st.metric(
    label="상위 그룹 평균 빈도",
    value=f"{avg_count:.1f}"
)

# 표 출력
st.dataframe(
    top_quartile,
    use_container_width=True,
    hide_index=True
)

# 그래프
st.bar_chart(
    top_quartile.set_index('태그')
)
