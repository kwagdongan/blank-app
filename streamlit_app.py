import streamlit as st
import pandas as pd

st.set_page_config(page_title="Steam 분석", layout="wide")

st.title("제목 테스트 중")
st.write("사이드바")

@st.cache_data
def load_data():
    return pd.read_csv('datas.csv', encoding='utf-8-sig')

# 세션에 데이터가 없으면 로드해서 저장
if 'df' not in st.session_state:
    st.session_state['df'] = load_data()

# 1. 데이터 로드 및 정제 후
df['genres_list'] = df['genres'].apply(clean_genres)

# [추가] 분석 시작 전 'Indie' 장르를 모든 행의 리스트에서 제거
df['genres_list'] = df['genres_list'].apply(lambda x: [g for g in x if g != 'Indie'])

# 2. 이후 전체 장르 빈도 분석 진행
df_genres = df.explode('genres_list')
# ... 이하 동일
