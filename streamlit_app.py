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

def clean_genres(genre_data):
    # NaN이거나 빈 값이면 빈 리스트 반환
    if pd.isna(genre_data) or genre_data == '':
        return []
    
    # 이미 리스트 형태라면 그대로 반환
    if isinstance(genre_data, list):
        return [g for g in genre_data if g != 'Indie']
    
    # 문자열 처리
    if isinstance(genre_data, str):
        if genre_data.startswith('['):
            try:
                data = ast.literal_eval(genre_data)
                return [g for g in data if g != 'Indie']
            except:
                clean = genre_data.replace('[', '').replace(']', '').replace("'", "").replace('"', '')
                data = [g.strip() for g in clean.split(',')]
                return [g for g in data if g != 'Indie' and g != '']
        else:
            data = [g.strip() for g in genre_data.split(',')]
            return [g for g in data if g != 'Indie' and g != '']
    
    return []

# 데이터 적용 (이 한 줄로 끝납니다)
df['genres_list'] = df['genres'].apply(clean_genres)
