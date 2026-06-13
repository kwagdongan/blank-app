import streamlit as st

st.title("게임 평가 분석")

# 1. 저장된 데이터 불러오기
df = st.session_state['df']

# 2. 'total_reviews' 기준 상위 10개 추출
# nlargest(n, 컬럼명)는 해당 컬럼의 값이 큰 순서대로 n개를 뽑아줍니다.
top10_games = df.nlargest(10, 'total_reviews')[['name', 'total_reviews']]

# 3. 화면에 출력
st.subheader("평가가 가장 많은 게임 Top 10")
st.dataframe(top10_games, use_container_width=True)
