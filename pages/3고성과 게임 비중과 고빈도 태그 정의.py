import streamlit as st
import pandas as pd
import ast
import altair as alt

st.title("고성과 게임 비중과 태그별 빈도수 분석")

# 데이터 불러오기
df = st.session_state['df'].copy()

# 숫자형 변환
df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
df['positive_percentual'] = pd.to_numeric(df['positive_percentual'], errors='coerce')





# -------------------------------
# 2. 성공 게임 정의
# -------------------------------

review_q3 = df['total_reviews'].quantile(0.50)
positive_q3 = df['positive_percentual'].quantile(0.50)

success_games = df[
    (df['total_reviews'] >= review_q3) &
    (df['positive_percentual'] >= positive_q3)
].copy()

# -------------------------------
# 3. 장르 펼치기
# -------------------------------

all_genres_exploded = df.explode('genres')
success_genres_exploded = success_games.explode('genres')



# -------------------------------
# 4. 전체 게임 수
# -------------------------------

total_count = (
    all_genres_exploded
    .groupby('genres')
    .size()
    .reset_index(name='전체게임수')
)

# -------------------------------
# 5. 성공 게임 수
# -------------------------------

success_count = (
    success_genres_exploded
    .groupby('genres')
    .size()
    .reset_index(name='고성과게임수')
)

# -------------------------------
# 6. 병합
# -------------------------------

result = pd.merge(
    total_count,
    success_count,
    on='genres',
    how='left'
)

result['고성과게임수'] = result['고성과게임수'].fillna(0)

# -------------------------------
# 7. 성공률 계산
# -------------------------------

result['고성과게임비중(%)'] = (
    result['고성과게임수']
    / result['전체게임수']
    * 100
)

# 표본 너무 적은 장르 제거
result = result[result['전체게임수'] >= 20]

# 성공률 순 정렬
result = result.sort_values(
    by='고성과게임비중(%)',
    ascending=False
)

# -------------------------------
# 8. 출력
# -------------------------------

st.subheader("고성과 태그 순위")

st.dataframe(
    result.head(10),
    use_container_width=True
)


st.info(
    "고성과 게임 비중 = 고성과 게임 수 / 전체 게임 수\n"
)
st.markdown("각 태그별 고성과 게임의 비중이 얼마나 되는 지를 알려줌")


st.markdown("---")


# 태그 펼치기
df_genres = df.explode('genres')

# 빈도 계산
genre_counts = df_genres['genres'].value_counts().reset_index()
genre_counts.columns = ['태그', '빈도']
genre_counts = genre_counts[genre_counts['태그'] != '']

# 상위 8%
q92 = genre_counts['빈도'].quantile(0.66)
top_group = genre_counts[genre_counts['빈도'] >= q92]

# 전체 평균
overall_avg = genre_counts['빈도'].mean()

st.subheader("태그 빈도 상위 그룹")

st.dataframe(
    top_group,
    use_container_width=True,
    hide_index=True
)

# 막대그래프
bars = alt.Chart(top_group).mark_bar().encode(
    x=alt.X(
        '빈도:Q',
        title='등장 빈도'
    ),
    y=alt.Y(
        '태그:N',
        sort='-x',
        title=None
    )
)

# 평균선
avg_line = alt.Chart(
    pd.DataFrame({'평균': [overall_avg]})
).mark_rule().encode(
    x='평균:Q'
)

chart = (
    bars + avg_line
).properties(
    height=400
)

st.altair_chart(
    chart,
    use_container_width=True
)

st.caption(
    f"선은 전체 태그 평균 빈도를 의미함.({overall_avg:.1f})"
)

st.markdown("빈도가 높은 태그는 경쟁이 높은 태그로 해석함")



q1 = genre_counts['빈도'].quantile(0.25)
q3 = genre_counts['빈도'].quantile(0.75)

iqr = q3 - q1

threshold = q3 + 1.5 * iqr

red_ocean_tags = genre_counts[
    genre_counts['빈도'] >= threshold
]['태그'].tolist()
