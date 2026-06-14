import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 분석 지표 정의")

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

st.subheader("분석에 사용된 지표")

metrics_df = pd.DataFrame({
    "지표": [
        "총 리뷰 수",
        "긍정 평가 비율",
        "태그 빈도"
    ],
    "의미": [
        "사용자 관심도",
        "사용자 만족도",
        "시장 경쟁 정도"
    ],
    "분석 목적": [
        "시장 반응 측정",
        "게임 품질 평가",
        "레드오션 판단"
    ]
})

st.dataframe(
    metrics_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ==========================
# 요약 통계
# ==========================

st.subheader("📈 데이터 요약")

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
# 리뷰 수 분포
# ==========================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🔥 총 리뷰 수 분포")

    # 로그 변환
    review_log = np.log10(
        df['total_reviews'] + 1
    )

    review_bins = pd.cut(
        review_log,
        bins=15
    )

    review_counts = (
        review_bins
        .value_counts()
        .sort_index()
    )

    review_df = pd.DataFrame({
        "구간": review_counts.index.astype(str),
        "게임 수": review_counts.values
    })

    st.bar_chart(
        review_df.set_index("구간")
    )

    st.caption(
        "리뷰 수는 사용자 관심도를 나타낸다. "
        "그래프는 로그 변환 후 시각화하였다."
    )

# ==========================
# 긍정 평가 비율 분포
# ==========================

with col2:

    st.subheader("👍 긍정 평가 비율 분포")

    positive_bins = pd.cut(
        df['positive_percentual'],
        bins=np.arange(0, 105, 5)
    )

    positive_counts = (
        positive_bins
        .value_counts()
        .sort_index()
    )

    positive_df = pd.DataFrame({
        "구간": positive_counts.index.astype(str),
        "게임 수": positive_counts.values
    })

    st.bar_chart(
        positive_df.set_index("구간")
    )

    st.caption(
        "긍정 평가 비율은 사용자 만족도를 나타낸다."
    )

st.markdown("---")

st.info("""
본 연구에서는

• 총 리뷰 수 → 사용자 관심도

• 긍정 평가 비율 → 사용자 만족도

로 정의하였다.

이후 두 지표가 모두 높은 게임들을 고성과 게임군으로 정의하여 분석을 진행한다.
""")
