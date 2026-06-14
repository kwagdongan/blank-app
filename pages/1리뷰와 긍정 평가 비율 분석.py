import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 분석 지표 정의")

# 데이터 가져오기
df = st.session_state['df'].copy()

# 숫자형 변환
df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
df['positive_percentual'] = pd.to_numeric(df['positive_percentual'], errors='coerce')

df = df.dropna(subset=['total_reviews', 'positive_percentual'])

# ==========================
# 지표 설명
# ==========================

st.subheader("분석에 사용된 지표")

metrics_df = pd.DataFrame({
    "지표": ["총 리뷰 수", "긍정 평가 비율", "태그 빈도"],
    "의미": ["사용자 관심도", "사용자 만족도", "시장 경쟁 정도"],
    "분석 목적": ["시장 반응 측정", "게임 품질 평가", "레드오션 판단"]
})

st.dataframe(
    metrics_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# 분포 그래프
# ==========================

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 총 리뷰 수 분포")

    review_hist = pd.cut(
        df['total_reviews'],
        bins=20
    ).value_counts().sort_index()

    st.bar_chart(review_hist)

    st.caption(
        "리뷰 수는 게임에 대한 사용자 관심도를 나타내는 지표로 사용하였다."
    )

with col2:
    st.subheader("👍 긍정 평가 비율 분포")

    positive_hist = pd.cut(
        df['positive_percentual'],
        bins=np.arange(0, 105, 5)
    ).value_counts().sort_index()

    st.bar_chart(positive_hist)

    st.caption(
        "긍정 평가 비율은 게임에 대한 사용자 만족도를 나타내는 지표로 사용하였다."
    )

st.markdown("---")

# ==========================
# 요약 통계
# ==========================

st.subheader("요약 통계")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "게임 수",
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

with c4:
    st.metric(
        "중앙값 리뷰 수",
        f"{int(df['total_reviews'].median()):,}"
    )

st.info("""
본 연구에서는

• 총 리뷰 수 → 사용자 관심도

• 긍정 평가 비율 → 사용자 만족도

로 정의하였다.

이후 두 지표가 모두 높은 게임들을 고성과 게임군으로 정의하여 분석을 진행한다.
""")
