import streamlit as st
import pandas as pd
import ast
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import altair as alt

st.set_page_config(page_title="Steam 분석", layout="wide")


st.title("Steam 게임 시장 장르별 빈도와 리뷰를 이용한 군집 분석")

st.markdown("---")


st.header("1. 연구 배경")
st.markdown("""
Steam에는 수만 개의 게임이 등록되어 있으며 매년 새로운 게임이 지속적으로 출시되고 있습니다.

이처럼 경쟁이 심화되는 환경에서는 단순히 인기 장르를 선택하는 것보다,
시장 내 경쟁 수준과 사용자 반응을 함께 고려한 장르 선택이 중요합니다.

따라서 데이터 기반으로 Steam 시장의 구조를 분석하고,
장르별 특성을 파악할 필요가 있습니다.
""")
    
st.header("2. 연구 목적")
st.markdown("""
본 연구의 목적은 Steam 게임 데이터를 분석하여 장르별로 경쟁 정도와 리뷰를 식별하여 군집 정보를 파악합니다.

""")
st.markdown("파악된 정보는 저를 포함한 게임 개발자들의 추후 게임 개발 정보로 활용됩니다. ")


st.header("3. 분석 방법")
st.markdown("""
Steam 게임 데이터의 태그(장르), 리뷰 수, 긍정 평가 비율 수치를 활용하였습니다.

- 리뷰 수와 긍정 평가 비율을 조절해 게임군(기준치 이상 게임군) 식별
- 태그별 기준치 이상 게임 수를 전체 게임 수로 나누어 태그별 기준치 이상 게임 비중 산출
- 태그별 게임 출시 수를 통해 시장 내 경쟁 밀도 산출
- 태그별 경쟁 밀도와 태그별 기준치 이상 게임 비중을 이용하여 //블루오션 후보// 태그 식별
""")
    

st.markdown("---")









EXCLUDED_TAGS = {
    "Indie", "Early Access", "Free To Play", "Software Training", 
    "Game Development", "Audio Production", "Utilities", "Photo Editing", 
    "Video Production", "Design & Illustration", "Sexual Content", 
    "Nudity", "Animation & Modeling", "Web Publishing"
}

# 0부터 100까지의 숫자를 문자열로 변환하여 추가
numbers_to_add = {str(i) for i in range(101)}

# 기존 집합(set)에 업데이트
EXCLUDED_TAGS.update(numbers_to_add)




@st.cache_data
def load_data():
    return pd.read_csv('datas.csv', encoding='utf-8-sig')

# 세션에 데이터가 없으면 로드해서 저장
if 'df' not in st.session_state:
    st.session_state['df'] = load_data()




def load_and_clean_data():
    df = pd.read_csv('datas.csv', encoding='utf-8-sig')
    # 1. total_reviews를 숫자로 강제 변환
    # errors='coerce'를 쓰면 숫자로 바꿀 수 없는 값은 자동으로 NaN(결측치)으로 변합니다.
    df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
    
    # 2. total_reviews가 NaN인 행(숫자가 아니었던 행들)은 아예 삭제합니다.
    df_cleaned = df.dropna(subset=['total_reviews'])
    
    return df_cleaned

# 데이터 로드
df = load_and_clean_data()



def clean_genres(genre_data):
    if pd.isna(genre_data) or genre_data == '': 
        return []
    
    # 문자열 처리
    if isinstance(genre_data, str):
        if genre_data.startswith('['):
            try:
                # 리스트 형태의 문자열 처리
                data = ast.literal_eval(genre_data)
            except:
                # 실패 시 쉼표로 분리
                clean = genre_data.replace('[', '').replace(']', '').replace("'", "").replace('"', '')
                data = clean.split(',')
        else:
            data = genre_data.split(',')
    elif isinstance(genre_data, list):
        data = genre_data
    else:
        return []
    
    # [핵심] 리스트 안에서 공백 제거 + 제외 키워드 삭제
    return [g.strip() for g in data if g.strip() != '' and g.strip() not in EXCLUDED_TAGS]


# 덮어쓰기 (중요: 여기서 genres 컬럼 자체를 리스트 값으로 바꿔버림)
df['genres'] = df['genres'].apply(clean_genres)
df = df.nlargest(10000, 'total_reviews')
st.session_state['df'] = df



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

st.sidebar.header("리뷰-긍정평가율 설정")

review_percentile = st.sidebar.slider(
    "리뷰 수 기준 백분위 (%)",
    min_value=50,
    max_value=95,
    value=75,
    step=5
)

positive_percentile = st.sidebar.slider(
    "긍정 평가 비율 기준 백분위 (%)",
    min_value=5,
    max_value=95,
    value=50,

)


review_threshold = df['total_reviews'].quantile(
    review_percentile / 100
)

positive_threshold = df['positive_percentual'].quantile(
    positive_percentile / 100
)

high_perf = df[
    (df['total_reviews'] >= review_threshold)
    &
    (df['positive_percentual'] >= positive_threshold)
].copy()





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
            title='태그별 기준치 이상 게임 비중'
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
        y='태그별기준치이상게임비중:Q',
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
    y=alt.Y('기준치이상게임비중:Q', scale=alt.Scale(domain=[0, tag_df['고성과게임비중'].max()]))
)
    

st.altair_chart(
    chart,
    use_container_width=True
)




# 클러스터별 데이터 요약 (인덱스 및 통계 정보)
cluster_summary = tag_df.groupby('cluster').agg({
    '태그': list,
    '전체빈도': ['mean'],
    '고성과게임비중': ['mean']
})

with st.expander("포지셔닝 맵 해석 가이드"):
    st.write("""
    * **고빈도-고비중 (우상단):** 시장의 주류이자 성공 법칙이 검증된 **'스테디셀러 영역'**.
    * **저빈도-고비중 (좌상단):** 경쟁은 적지만 성과는 높은 **'블루오션 기회 영역'**.
    * **고빈도-저비중 (우하단):** 경쟁은 치열하나 성과를 내기 힘든 **'레드오션 영역'**.
    * **저빈도-저비중 (좌하단):** 유저 반응이 아직 확인되지 않은 **'실험적 영역'**.
    """)


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





st.markdown("---")


st.subheader("데이터 출처 및 라이선스")
st.info("""
본 분석은 **Valve Corporation**에서 제공하는 **Steam Web API**를 활용하였습니다.
- 데이터 출처: Steam Web API (https://partner.steamgames.com/doc/webapi)
""")

