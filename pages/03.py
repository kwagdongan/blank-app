import streamlit as st
import pandas as pd
import ast

st.title("장르별 게임 분포 분석")

# 1. 데이터 로드 및 정제
df = st.session_state['df'].copy()

def clean_genres(genre_data):
    if pd.isna(genre_data) or genre_data == '':
        return []
    
    # 리스트 형태의 문자열(예: "['Action', 'RPG']")인 경우
    if isinstance(genre_data, str) and genre_data.startswith('['):
        try:
            return ast.literal_eval(genre_data)
        except:
            # 실패 시 특수문자 제거
            clean = genre_data.replace('[', '').replace(']', '').replace("'", "").replace('"', '')
            return [g.strip() for g in clean.split(',')]
    
    # 이미 콤마로 구분된 문자열인 경우
    return [g.strip() for g in genre_data.split(',')]

# 장르 정제 적용
df['genres_list'] = df['genres'].apply(clean_genres)

# 2. 데이터 펼치기
df_genres = df.explode('genres_list')

# 3. 빈도 분석
genre_counts = df_genres['genres_list'].value_counts().reset_index()
genre_counts.columns = ['Genre', 'Count']
genre_counts = genre_counts[genre_counts['Genre'] != ''] # 빈 값 제거

# 4. 결과 출력
st.subheader("장르별 게임 수 Top 5")
st.dataframe(genre_counts.head(5), use_container_width=True)

# 5. 시각화
st.bar_chart(genre_counts.head(10).set_index('Genre'))

