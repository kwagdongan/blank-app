import streamlit as st
import pandas as pd
import ast

st.title("진정한 블루오션 장르 발굴")

# 1. 데이터 로드 및 정제
df = st.session_state['df'].copy()
df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
df['positive_percentual'] = pd.to_numeric(df['positive_percentual'], errors='coerce')
df = df[(df['total_reviews'] > 0) & (df['positive_percentual'] > 0)].copy()

# 장르 정제 함수
def clean_genres(genre_data):
    if pd.isna(genre_data) or genre_data == '': return []
    if isinstance(genre_data, str) and genre_data.startswith('['):
        try: return ast.literal_eval(genre_data)
        except: return [g.strip() for g in genre_data.replace('[', '').replace(']', '').replace("'", "").split(',')]
    return [g.strip() for g in genre_data.split(',')]

df['genres_list'] = df['genres'].apply(clean_genres)

# 2. [핵심] 전체 데이터 기준 레드오션(Top 10) 확정
all_genres = df.explode('genres_list')
top10_red_ocean = all_genres['genres_list'].value_counts().nlargest(10).index.tolist()

st.write(f"🛑 제외된 레드오션 장르(Top 10): {', '.join(top10_red_ocean)}")

# 3. 제1사분면(성공군) 데이터만 필터링
review_q3 = df['total_reviews'].quantile(0.75)
positive_q3 = df['positive_percentual'].quantile(0.75)
q1_games = df[(df['total_reviews'] >= review_q3) & (df['positive_percentual'] >= positive_q3)].copy()

# 4. 필터링 적용: 성공군 장르에서 레드오션 장르 제거
q1_genres = q1_games.explode('genres_list')
blue_ocean_candidates = q1_genres[~q1_genres['genres_list'].isin(top10_red_ocean)]

# 5. 빈도 분석
blue_ocean_result = blue_ocean_candidates['genres_list'].value_counts().reset_index()
blue_ocean_result.columns = ['Genre', 'Count']

st.subheader("진정한 블루오션 장르 리스트")
st.dataframe(blue_ocean_result, use_container_width=True)
