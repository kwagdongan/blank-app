import streamlit as st
import pandas as pd

st.title("가장 인기 있는 태그 분석")

# 1. 세션에서 데이터 가져오기
df = st.session_state['df'].copy()

# 2. 태그 데이터 정제 및 분리
# 태그가 쉼표(,)로 구분되어 있다고 가정합니다. (혹시 구분자가 다르다면 말씀해주세요!)
# 예: "Action, Adventure, Indie" -> ["Action", "Adventure", "Indie"]
df['genres'] = df['genres'].fillna('') # 빈 값 처리
df['tags_list'] = df['genres'].str.split(',') 

# 3. 데이터 펼치기 (Explode)
# 하나의 행을 태그 개수만큼 여러 행으로 복제합니다.
df_tags = df.explode('tags_list')

# 4. 앞뒤 공백 제거 및 대문자 통일 (정확한 카운팅을 위해)
df_tags['tags_list'] = df_tags['tags_list'].str.strip().str.lower()

# 5. 태그별 빈도 계산
tag_counts = df_tags['tags_list'].value_counts().reset_index()
tag_counts.columns = ['Tag', 'Count']

# 6. 결과 출력
st.subheader("태그별 등장 횟수 Top 20")
st.dataframe(tag_counts.head(20), use_container_width=True)

# 7. 시각화
st.subheader("태그 빈도 그래프")
st.bar_chart(tag_counts.head(20).set_index('Tag'))
