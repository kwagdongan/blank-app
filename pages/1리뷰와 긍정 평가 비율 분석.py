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

    st.subheader("총 리뷰 수 분포 (로그 스케일 적용)")

# 로그 스케일 적용을 위해 0인 데이터는 아주 작은 값으로 치환 (로그(0)은 정의되지 않음)
review_df = pd.DataFrame({
    "total_reviews": df['total_reviews'].replace(0, 0.1) 
})

review_chart = (
    alt.Chart(review_df)
    .mark_bar()
    .encode(
        x=alt.X(
            "total_reviews:Q",
            bin=alt.Bin(maxbins=50), # 구간을 좀 더 세밀하게 조정
            scale=alt.Scale(type='log'), # [핵심] 로그 스케일 적용
            title="총 리뷰 수 (Log Scale)"
        ),
        y=alt.Y(
            "count()",
            title="게임 수"
        )
    )
    .properties(height=350)
)

st.altair_chart(
    review_chart,
    use_container_width=True
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


