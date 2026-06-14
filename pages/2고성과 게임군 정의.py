import streamlit as st
import pandas as pd
import altair as alt

st.subheader("고성과 게임군 정의")

# 데이터 로드
df = st.session_state['df'].copy()

df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
df['positive_percentual'] = pd.to_numeric(df['positive_percentual'], errors='coerce')

df = df.dropna(subset=['total_reviews', 'positive_percentual'])

# 산점도
chart = (
    alt.Chart(df)
    .mark_circle(size=40)
    .encode(
        x=alt.X(
            'total_reviews:Q',
            title='총 리뷰 수'
        ),
        y=alt.Y(
            'positive_percentual:Q',
            title='긍정 평가 비율',
            axis=alt.Axis(
                titleAngle=0,
                titlePadding=20
            )
        ),
        tooltip=[
            alt.Tooltip('name:N', title='게임명'),
            alt.Tooltip('total_reviews:Q', title='총 리뷰 수', format=','),
            alt.Tooltip('positive_percentual:Q', title='긍정 평가 비율', format='.1f')
        ]
    )
    .properties(height=500)
)

st.altair_chart(chart, use_container_width=True)

st.markdown("---")



# ==========================
# 고성과 게임군 정의
# ==========================

review_q3 = df['total_reviews'].quantile(0.75)
positive_q3 = df['positive_percentual'].quantile(0.75)

high_perf = df[
    (df['total_reviews'] >= review_q3) &
    (df['positive_percentual'] >= positive_q3)
].copy()

st.markdown(
    f"""
    고성과 게임군은

    • 총 리뷰 수 상위 25% 이상

    • 긍정 평가 비율 상위 25% 이상

    을 동시에 만족하는 게임으로 정의함

    현재 고성과 게임군은 총 {len(high_perf):,}개
    """
)

# ==========================
# 고성과 게임 Top 5
# ==========================

st.subheader("고성과 게임 Top 5")

top5 = high_perf.nlargest(5, 'total_reviews')

st.dataframe(
    top5[['name', 'total_reviews', 'positive_percentual']],
    use_container_width=True,
    hide_index=True
)

# ==========================
# 고성과 게임군 태그 Top 10
# ==========================

st.subheader("고성과 게임군 태그 Top 10")

high_perf_tags = high_perf.explode('genres')

tag_counts = (
    high_perf_tags['genres']
    .value_counts()
    .head(10)
    .reset_index()
)

tag_counts.columns = ['태그', '게임 수']

tag_chart = (
    alt.Chart(tag_counts)
    .mark_bar()
    .encode(
        x=alt.X(
            '게임 수:Q',
            title='게임 수'
        ),
        y=alt.Y(
            '태그:N',
            sort='-x',
            title=None
        ),
        tooltip=[
            '태그',
            '게임 수'
        ]
    )
    .properties(height=350)
)

st.altair_chart(tag_chart, use_container_width=True)

