import streamlit as st
import pandas as pd
import altair as alt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

st.title("기준치 이상 게임군 정의")

st.markdown("""
사용자가 직접 리뷰 수와 긍정 평가 비율 기준을 조정하여
게임군이 어떻게 변화하는지 확인할 수 있습니다.
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

st.sidebar.header("리뷰-긍정평가율")
st.sidebar.header("기준치 이상 게임군 설정")

review_percentile = st.sidebar.slider(
    "리뷰 수 기준 백분위 (%)",
    min_value=50,
    max_value=95,
    value=50,
    step=5
)

positive_percentile = st.sidebar.slider(
    "긍정 평가 비율 기준 백분위 (%)",
    min_value=5,
    max_value=95,
    value=50,
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
        "기준치 이상 게임 수",
        len(high_perf)
    )

st.markdown("---")

# -------------------
# 산점도
# -------------------

st.subheader("리뷰수와 긍정 평가 비율 분포")

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


st.markdown("기준치 이상 게임군의 태그 비중")

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


st.info(
    """
    슬라이더를 조정하면 기준치 이상 게임군이 변경되며,
    이에 따라 포함되는 게임과 게임 수가 실시간으로 변합니다.
    """
)







st.markdown("---")
st.subheader("태그 포지셔닝 맵")



# ======================
# 고성과 게임군 정의
# ======================
review_q3 = review_threshold
positive_q3 = positive_threshold

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





# 데이터 표준화
scaler = StandardScaler()
scaled_data = scaler.fit_transform(tag_df[['전체빈도', '고성과게임비중']])

# 군집화 수행
kmeans = KMeans(n_clusters=4, random_state=42)
tag_df['cluster'] = kmeans.fit_predict(scaled_data).astype(str)









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
            title='태그별 고성과 게임 비중'
        ),
        color='cluster:N',  # [핵심] 군집별 색상 구분
        tooltip=[
            alt.Tooltip('태그:N'),
            alt.Tooltip('전체빈도:Q', format=','),
            alt.Tooltip('태그별기준치이상게임비중:Q', format='.3f')
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
        y='태그별고성과게임비중:Q',
        text='태그:N'
    )
)


chart = (points +
    text +
    vline +
    hline
).properties(
    width=600,   # 가로 폭 고정
    height=600   # 세로 높이를 가로와 동일하게 설정
).encode(
    
)



chart = chart.encode(
    x=alt.X('전체빈도:Q', scale=alt.Scale(domain=[0, tag_df['전체빈도'].max()])),
    y=alt.Y('고성과게임비중:Q', scale=alt.Scale(domain=[0, tag_df['고성과게임비중'].max()]))
)
    

st.altair_chart(
    chart,
    use_container_width=True
)

st.info("태그별 기준치 이상 게임 비율 = 기준치 이상 게임수/전체 게임수")

with st.expander("포지셔닝 맵 해석 가이드"):
    st.write("""
    * **고빈도-고비중 (우상단):** 시장의 주류이자 성공 법칙이 검증된 **'스테디셀러 영역'**.
    * **저빈도-고비중 (좌상단):** 경쟁은 적지만 성과는 높은 **'블루오션 기회 영역'**.
    * **고빈도-저비중 (우하단):** 경쟁은 치열하나 성과를 내기 힘든 **'레드오션 영역'**.
    * **저빈도-저비중 (좌하단):** 유저 반응이 아직 확인되지 않은 **'실험적 영역'**.
    """)

st.markdown("---")

# 클러스터별 데이터 요약 (인덱스 및 통계 정보)
cluster_summary = tag_df.groupby('cluster').agg({
    '태그': list,
    '전체빈도': ['mean', 'min', 'max'],
    '고성과게임비중': ['mean', 'min', 'max']
})

# 인덱스 값 확인
st.write(cluster_summary)



total_games = len(df)
high_perf_count = len(high_perf)
high_perf_ratio = (high_perf_count / total_games) * 100 if total_games > 0 else 0


# 4. 사이드바에 지표 표시
st.sidebar.markdown("---")
st.sidebar.metric("전체 분석 대상", f"{total_games:,}개")
st.sidebar.metric("기준치 이상 게임 수", f"{high_perf_count:,}개")
st.sidebar.metric("기준치 이상 게임 비율", f"{high_perf_ratio:.1f}%")
st.sidebar.markdown("---")









