import streamlit as st
import pandas as pd

st.subheader("긍정 비율 vs 리뷰 수 2차원 분석")
df = pd.read_csv('datas.csv', encoding='utf-8-sig')

# 산점도를 위한 데이터 준비 (인터랙티브한 그래프)
st.scatter_chart(
    df, 
    x='total_reviews', 
    y='positive_percentual',
    # 마우스 올리면 게임 이름이 보이게 설정
    size=None, 
    color=None 
)

st.write("💡 **분석 팁:** 오른쪽 상단(리뷰도 많고, 긍정 비율도 높은 영역)에 위치한 게임들이 시장을 주도하는 긍정적 지표를 가진 게임들입니다.")
