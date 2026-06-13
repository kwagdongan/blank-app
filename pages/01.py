import streamlit as st
import pandas as pd

@st.cache_data
def load_and_clean_data():
    df = pd.read_csv('datas.csv', encoding='cp949')
    
    # 1. total_reviews를 숫자로 강제 변환
    # errors='coerce'를 쓰면 숫자로 바꿀 수 없는 값은 자동으로 NaN(결측치)으로 변합니다.
    df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
    
    # 2. total_reviews가 NaN인 행(숫자가 아니었던 행들)은 아예 삭제합니다.
    df_cleaned = df.dropna(subset=['total_reviews'])
    
    # 3. 데이터가 잘 정제되었는지 확인하기 위해 상위 5개 출력 (디버깅용)
    return df_cleaned

# 데이터 로드
df = load_and_clean_data()

# 4. 평가 많은 순 상위 10개 추출
top10_games = df.nlargest(10, 'total_reviews')[['name', 'total_reviews']]

st.dataframe(top10_games)
