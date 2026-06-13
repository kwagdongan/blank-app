import streamlit as st
import pandas as pd

# 1. 데이터 불러오기
@st.cache_data  # 데이터를 메모리에 캐싱하여 속도 향상
def load_data():
    df = pd.read_csv('datas.csv')
    
    # [데이터 정제 핵심 단계]
    # 1. 문자열로 되어있을 수 있는 total_reviews를 숫자로 변환 (오류 시 NaN 처리)
    df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
    
    # 2. 결측치(NaN) 제거 (평가 수가 없는 게임은 분석에서 제외)
    df = df.dropna(subset=['total_reviews'])
    
    # 3. 데이터가 너무 많으면 상위 10개 추출 시 오류 방지를 위해 형식 유지
    return df

# 데이터 로드 및 세션 저장
if 'df' not in st.session_state:
    st.session_state['df'] = load_data()

df = st.session_state['df']
