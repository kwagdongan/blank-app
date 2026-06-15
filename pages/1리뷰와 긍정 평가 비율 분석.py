import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title("리뷰와 긍정 평가 비율 분석")

# ==========================
# 데이터 로드
# ==========================

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

# ==========================
# 지표 설명
# ==========================

st.markdown("---")

# ==========================
# 요약 통계
# ==========================

st.subheader("데이터 요약")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "전체 게임 수",
        f"{len(df):,}"
    )

with c2:
    st.metric(
        "평균 리뷰 수",
        f"{int(df['total_reviews'].mean()):,}"
    )

with c3:
    st.metric(
        "평균 긍정 비율",
        f"{df['positive_percentual'].mean():.1f}%"
    )

st.markdown("---")

# ==========================
# 히스토그램
# ==========================

col1, col2 = st.columns(2)

# 리뷰 수
with col1:

    st.subheader("총 리뷰 수 분포 (사용자 관심도로 해석)")

    review_df = pd.DataFrame({
        "log_reviews": 
            df['total_reviews']
        )
    })

    review_chart = (
        alt.Chart(review_df)
        .mark_bar()
        .encode(
            x=alt.X(
                "log_reviews:Q",
                bin=alt.Bin(maxbins=30),
                title="로그 변환 된 총 리뷰 수"
            ),
            y=alt.Y(
                "count()",
                title=None
            )
        )
        .properties(height=350)
    )

    st.altair_chart(
        review_chart,
        use_container_width=True
    )

    st.caption(
        "총 리뷰수 값의 편차가 커 로그 변환 후 시각화"
    )

# 긍정 비율
with col2:

    st.subheader("긍정 평가 비율 분포 (사용자 만족도로 해석)")

    positive_df = df[df['positive_percentual'] > 0]
    
    positive_chart = (
        alt.Chart(positive_df)
        .mark_bar()
        .encode(
            x=alt.X(
                "positive_percentual:Q",
                bin=alt.Bin(step=5),
                title="긍정 평가 비율 (%)"
            ),
            y=alt.Y(
                "count()",
                title=None
            )
        )
        .properties(height=350)
    )

    st.altair_chart(
        positive_chart,
        use_container_width=True
    )

    

st.markdown("---")


