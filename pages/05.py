import streamlit as st
import pandas as pd
import ast

st.title("전체 장르 분포 현황")

# 1. 데이터 로드
df = st.session_state['df'].copy()

# 2. 장르 데이터 정제 및 리스트화
def clean_genres(genre_data):
    if pd.isna(genre_data) or genre_data == '': return []
    if isinstance(genre_data, str) and genre_data.startswith('['):
        try: return ast.literal_eval(genre_data)
        except: return [g.strip() for g in genre_data.replace('[', '').replace(']', '').replace("'", "").split(',')]
    return [g.strip() for g in genre_data.split(',')]

df['genres_list'] = df['genres'].apply(clean_genres)

# 3. 데이터 펼치기 (explode)
all_genres = df.explode('genres_list')
all_genres = all_genres[all_genres['genres_list'] != ''] # 빈 값 제거

# 4. 빈도 계산
genre_counts = all_genres['genres_list'].value_counts().reset_index()
genre_counts.columns = ['장르명', '게임 수']

# 5. 화면 출력
st.subheader("모든 장르 한눈에 보기")
st.write(f"현재 총 {len(genre_counts)}개의 고유 장르가 등록되어 있습니다.")

# 사용자가 클릭해서 정렬할 수 있게 표시
st.dataframe(genre_counts, use_container_width=True)

# 6. 간단한 시각화
st.subheader("장르별 게임 개수 분포")
st.bar_chart(genre_counts.set_index('장르명'))
