import streamlit as st
import pandas as pd
import altair as alt

st.title("고성과 게임군 기준 탐색")

st.markdown("""
사용자가 직접 리뷰 수와 긍정 평가 비율 기준을 조정하여
고성과 게임군이 어떻게 변화하는지 확인할 수 있습니다.
""")

# -------------------
# 데이터 로드
# -------------------

df = st.session_state['df'].copy()

df['total_reviews'] = pd.to_numeric(
    df['total_reviews'],
    errors='coerce'
)

df['positive_percentual'] = pd.to_numeric(
    df['positive_percentual'],
    errors='coerce'
)

df = df.dropna(
    subset=['total_reviews', 'positive_percentual']
)

# -------------------
# 슬라이더
# -------------------

st.sidebar.header("고성과 게임군 기준 설정")

review_percentile = st.sidebar.slider(
    "리뷰 수 기준 백분위 (%)",
    min_value=50,
    max_value=95,
    value=75,
    step=5
)

positive_percentile = st.sidebar.slider(
    "긍정 평가 비율 기준 백분위 (%)",
    min_value=50,
    max_value=95,
    value=75,
    step=5
)

# -------------------
# 기준 계산
# -------------------

review_threshold = df['total_reviews'].quantile(
    review_percentile / 100
)

positive_threshold = df['positive_percentual'].quantile(
    positive_percentile / 100
)

# -------------------
# 고성과 게임군 추출
# -------------------

high_perf = df[
    (df['total_reviews'] >= review_threshold)
    &
    (df['positive_percentual'] >= positive_threshold)
].copy()

# -------------------
# 기준 표시
# -------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "리뷰 수 기준",
        f"{review_threshold:,.0f}"
    )

with col2:
    st.metric(
        "긍정 평가 기준",
        f"{positive_threshold:.1f}%"
    )

with col3:
    st.metric(
        "고성과 게임 수",
        len(high_perf)
    )

st.markdown("---")

# -------------------
# 산점도
# -------------------

st.subheader("고성과 게임군 분포")

base = alt.Chart(df).mark_circle(
    size=40,
    opacity=0.25
).encode(
    x=alt.X(
        'total_reviews:Q',
        title='총 리뷰 수'
    ),
    y=alt.Y(
        'positive_percentual:Q',
        title='긍정 평가 비율 (%)'
    )
)

highlight = alt.Chart(high_perf).mark_circle(
    size=80
).encode(
    x='total_reviews:Q',
    y='positive_percentual:Q',
    tooltip=[
        alt.Tooltip('name:N', title='게임명'),
        alt.Tooltip(
            'total_reviews:Q',
            title='총 리뷰 수',
            format=','
        ),
        alt.Tooltip(
            'positive_percentual:Q',
            title='긍정 평가 비율',
            format='.1f'
        )
    ]
)

vline = alt.Chart(
    pd.DataFrame(
        {'x': [review_threshold]}
    )
).mark_rule().encode(
    x='x:Q'
)

hline = alt.Chart(
    pd.DataFrame(
        {'y': [positive_threshold]}
    )
).mark_rule().encode(
    y='y:Q'
)

chart = (
    base +
    highlight +
    vline +
    hline
).properties(
    height=600
)

st.altair_chart(
    chart,
    use_container_width=True
)

# -------------------
# 상위 게임 출력
# -------------------

st.subheader("고성과 게임 Top 20")

top_games = high_perf.nlargest(
    20,
    'total_reviews'
)

display_df = top_games[
    [
        'name',
        'total_reviews',
        'positive_percentual'
    ]
].copy()

display_df.columns = [
    '게임명',
    '총 리뷰 수',
    '긍정 평가 비율'
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.info(
    """
    슬라이더를 조정하면 고성과 게임군의 기준이 변경되며,
    이에 따라 포함되는 게임과 게임 수가 실시간으로 변합니다.
    """
)
