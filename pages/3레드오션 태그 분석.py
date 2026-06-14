import streamlit as st
import pandas as pd

st.title("태그별 게임 분포 분석")

# 데이터 로드
df = st.session_state['df']

# 데이터 펼치기
df_genres = df.explode('genres')

# 빈도 분석
genre_counts = df_genres['genres'].value_counts().reset_index()
genre_counts.columns = ['태그', '빈도']
genre_counts = genre_counts[genre_counts['태그'] != '']

# 상위 8%
q92 = genre_counts['빈도'].quantile(0.92)
top_group = genre_counts[genre_counts['빈도'] >= q92]

# 전체 평균 빈도
overall_avg = genre_counts['빈도'].mean()

st.subheader("태그 빈도 상위 그룹")

st.dataframe(
    top_group,
    use_container_width=True,
    hide_index=True
)

# 그래프 + 평균값
col1, col2 = st.columns([4, 1])

with col1:
    st.bar_chart(
        top_group.set_index('태그')
    )

with col2:
    st.metric(
        label="전체 평균 빈도",
        value=f"{overall_avg:.1f}"
    )

    st.caption("전체 태그의 평균 등장 횟수")
