import streamlit as st
import pandas as pd

st.title("블루오션 장르 발굴")

# 데이터 불러오기
df = st.session_state['df'].copy()

# 숫자형 변환
df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
df['positive_percentual'] = pd.to_numeric(df['positive_percentual'], errors='coerce')





# -------------------------------
# 2. 성공 게임 정의
# -------------------------------

review_q3 = df['total_reviews'].quantile(0.50)
positive_q3 = df['positive_percentual'].quantile(0.50)

success_games = df[
    (df['total_reviews'] >= review_q3) &
    (df['positive_percentual'] >= positive_q3)
].copy()

# -------------------------------
# 3. 장르 펼치기
# -------------------------------

all_genres_exploded = df.explode('genres')
success_genres_exploded = success_games.explode('genres')



# -------------------------------
# 4. 전체 게임 수
# -------------------------------

total_count = (
    all_genres_exploded
    .groupby('genres')
    .size()
    .reset_index(name='전체게임수')
)

# -------------------------------
# 5. 성공 게임 수
# -------------------------------

success_count = (
    success_genres_exploded
    .groupby('genres')
    .size()
    .reset_index(name='고성과게임수')
)

# -------------------------------
# 6. 병합
# -------------------------------

result = pd.merge(
    total_count,
    success_count,
    on='genres',
    how='left'
)

result['고성과게임수'] = result['고성과게임수'].fillna(0)

# -------------------------------
# 7. 성공률 계산
# -------------------------------

result['고성과률(%)'] = (
    result['고성과게임수']
    / result['전체게임수']
    * 100
)

# 표본 너무 적은 장르 제거
result = result[result['전체게임수'] >= 20]

# 성공률 순 정렬
result = result.sort_values(
    by='고성과률(%)',
    ascending=False
)

# -------------------------------
# 8. 출력
# -------------------------------

st.subheader("블루오션 장르 순위")

st.dataframe(
    result.head(10),
    use_container_width=True
)


st.info(
    "고성과률 = 고성과 게임 수 / 전체 게임 수\n"
)
