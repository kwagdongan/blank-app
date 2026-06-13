import streamlit as st
import pandas as pd

st.title("긍정 비율이 높은 게임 분석")

# 1. 데이터 로드 및 정제
@st.cache_data
def load_data():
    df = pd.read_csv('datas.csv', encoding='cp949') # 인코딩 상황에 맞게 조정
    
    # 숫자 변환
    df['positive_percentual'] = pd.to_numeric(df['positive_percentual'], errors='coerce')
    df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
    
    # NaN 제거
    df = df.dropna(subset=['positive_percentual', 'total_reviews'])
    return df

df = load_data()

# 2. 분석 로직
# 긍정 비율 100%인 게임 중, 리뷰 수가 많은 순서대로 상위 10개 추출
top_positive_games = df[df['positive_percentual'] == 100].sort_values(by='total_reviews', ascending=False).head(10)

# 3. 화면 출력
st.subheader("긍정 비율 100% & 리뷰 많은 순 Top 10")
st.dataframe(top_positive_games[['name', 'positive_percentual', 'total_reviews']], use_container_width=True)
