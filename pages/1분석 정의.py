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


st.subheader("총 리뷰 수 분포")

# 1. 슬라이더 추가: 리뷰 수 상한값 조절
# 데이터의 최대값을 슬라이더의 기본값으로 설정
max_review = int(df['total_reviews'].max())
selected_max = st.slider(
    "리뷰 수 표시 범위 조절 (상한선)", 
    min_value=100, 
    max_value=max_review, 
    value=max_review // 10, # 처음에는 전체의 1/10 정도로 좁게 보여줌
    step=100
)



# 2. 데이터 필터링
filtered_df = df[df['total_reviews'] <= selected_max]

# 3. 차트 생성
review_chart = (
    alt.Chart(filtered_df)
    .mark_bar()
    .encode(
        x=alt.X(
            "total_reviews:Q",
            bin=alt.Bin(maxbins=30),
            title="총 리뷰 수"
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
    
st.markdown("리뷰수는 게임에 대한 의견 제출이므로 사용자의 관심도로 해석할 수 있습니다.")
    

# 긍정 비율
st.subheader("긍정 평가 비율 분포")

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
.properties(height=350))

st.altair_chart(
positive_chart,
use_container_width=True
    )
st.markdown("""
리뷰의 긍정 평가 비율은 게임에 대한 만족도이므로 사용자 만족도로 해석할 수 있습니다.
""")
    

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

st.markdown("빈도가 높은 태그는 경쟁이 높은 태그로 해석합니다.")



q1 = genre_counts['빈도'].quantile(0.25)
q3 = genre_counts['빈도'].quantile(0.75)

iqr = q3 - q1

threshold = q3 + 1.5 * iqr

red_ocean_tags = genre_counts[
    genre_counts['빈도'] >= threshold
]['태그'].tolist()

