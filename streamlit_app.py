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

# 기존 정제 코드 바로 밑에 추가
df['genres_list'] = df['genres'].apply(clean_genres)

# [핵심] 'Indie' 제거: 모든 장르 리스트에서 'Indie' 삭제
df['genres_list'] = df['genres_list'].apply(lambda x: [g for g in x if g != 'Indie'])

# 이후 df_genres를 explode 하세요
df_genres = df.explode('genres_list')
