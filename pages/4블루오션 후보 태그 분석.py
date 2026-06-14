import streamlit as st
import pandas as pd
import altair as alt

st.subheader("태그 포지셔닝 맵")

df = st.session_state['df'].copy()

# 숫자형 변환
df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
df['positive_percentual'] = pd.to_numeric(df['positive_percentual'], errors='coerce')

df = df.dropna(subset=['total_reviews', 'positive_percentual'])

# ======================
# 고성과 게임군 정의
# ======================
review_q3 = df['total_reviews'].quantile(0.75)
positive_q3 = df['positive_percentual'].quantile(0.75)

high_perf = df[
    (df['total_reviews'] >= review_q3) &
    (df['positive_percentual'] >= positive_q3)
]

# ======================
# 전체 태그 빈도
# ======================
all_tags = df.explode('genres')

total_tag_count = (
    all_tags['genres']
    .value_counts()
    .reset_index()
)

total_tag_count.columns = ['태그', '전체빈도']

# ======================
# 고성과 게임 태그 빈도
# ======================
high_tags = high_perf.explode('genres')

high_tag_count = (
    high_tags['genres']
    .value_counts()
    .reset_index()
)

high_tag_count.columns = ['태그', '고성과빈도']

# ======================
# 결합
# ======================
tag_df = pd.merge(
    total_tag_count,
    high_tag_count,
    on='태그',
    how='left'
)

tag_df['고성과빈도'] = tag_df['고성과빈도'].fillna(0)

# 고성과 게임 비중
tag_df['고성과게임비중'] = (
    tag_df['고성과빈도']
    / tag_df['전체빈도']
)

tag_df = tag_df[tag_df['고성과게임비중'] > 0]
# 기준선
x_mean = tag_df['전체빈도'].mean()
y_mean = tag_df['고성과게임비중'].mean()

# ======================
# 산점도
# ======================
points = (
    alt.Chart(tag_df)
    .mark_circle(size=120)
    .encode(
        x=alt.X(
            '전체빈도:Q',
            title='태그 빈도 (경쟁도)'
        ),
        y=alt.Y(
            '고성과게임비중:Q',
            title='고성과 게임 비중'
        ),
        tooltip=[
            alt.Tooltip('태그:N'),
            alt.Tooltip('전체빈도:Q', format=','),
            alt.Tooltip('고성과게임비중:Q', format='.3f')
        ]
    )
)

text = (
    alt.Chart(tag_df)
    .mark_text(
        dx=10,
        dy=-5
    )
    .encode(
        x='전체빈도:Q',
        y='고성과게임비중:Q',
        text='태그:N'
    )
)

# 세로선
vline = alt.Chart(
    pd.DataFrame({'x': [x_mean]})
).mark_rule().encode(
    x='x:Q'
)

# 가로선
hline = alt.Chart(
    pd.DataFrame({'y': [y_mean]})
).mark_rule().encode(
    y='y:Q'
)

chart = (
    points +
    text +
    vline +
    hline
).properties(
    height=650
)

st.altair_chart(
    chart,
    use_container_width=True
)

st.info("""
제2사분면(좌상단):
경쟁도는 낮지만 고성과 게임 비중이 높은 태그.
본 연구에서는 해당 영역을 블루오션 후보 영역으로 해석한다.
""")
