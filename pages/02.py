import streamlit as st
import pandas as pd
import os

st.title("긍정적인 평가가 많은 게임 Top 10")

# 1. 데이터 로드 (인코딩 문제 방지)
@st.cache_data
def load_data():
    # 파일 경로 설정
    file_path = 'datas.csv'
    # 인코딩이 안 맞는 경우를 대비해 'cp949' 시도 후 실패 시 'utf-8-sig' 시도
    try:
        df = pd.read_csv(file_path, encoding='cp949')
    except:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    
    # total_positive를 숫자로 변환 (숫자 아닌 값은 NaN 처리)
    df['total_positive'] = pd.to_numeric(df['total_positive'], errors='coerce')
    
    # 결측치 제거
    df = df.dropna(subset=['total_positive'])
    return df

# 데이터 로드
df = load_data()

# 2. 'total_positive' 기준 상위 10개 추출
top10_positive = df.nlargest(10, 'total_positive')[['name', 'total_positive']]

# 3. 화면 출력
st.dataframe(top10_positive, use_container_width=True)

# 4. 차트 추가 (데이터 시각화)
st.subheader("그래프로 보기")
st.bar_chart(top10_positive.set_index('name'))
