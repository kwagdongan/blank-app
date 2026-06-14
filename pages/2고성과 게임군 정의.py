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

st.markdown("리뷰 수가 많고 긍정 평가 비율이 높은 게임은 사용자 관심도와 사용자 만족도가 높은 고성과 게임군으로 해석함")
