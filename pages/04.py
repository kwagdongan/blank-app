import streamlit as st
import pandas as pd
import ast

st.title("핵심 성공 장르 분석 (제1사분면 전략)")

# 1. 데이터 로드 및 0 초과 정제
df = st.session_state['df'].copy()
df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
df['positive_percentual'] = pd.to_numeric(df['positive_percentual'], errors='coerce')
df = df[(df['total_reviews'] > 0) & (df['positive_percentual'] > 0)].copy()

# 2. 제1사분면(리뷰 상위 25% & 긍정 비율 상위 25%) 정의
review_q3 = df['total_reviews'].quantile(0.75)
positive_q3 = df['positive_percentual'].quantile(0.75)

# 성공한 게임군 추출
q1_games = df[(df['total_reviews'] >= review_q3) & (df['positive_percentual'] >= positive_q3)].copy()

st.write(f"📊 성공 게임 정의: 리뷰 {review_q3:.0f}개 이상 & 긍정 비율 {positive_q3:.1f}% 이상")

# 3. 장르 데이터 정제 (genres 컬럼 사용)
def clean_genres(genre_data):
    if pd.isna(genre_data) or genre_data == '': return []
    # 리스트 문자열인 경우 처리
    if isinstance(genre_data, str) and genre_data.startswith('['):
        try: return ast.literal_eval(genre_data)
        except: return [g.strip() for g in genre_data.replace('[', '').replace(']', '').replace("'", "").split(',')]
    return [g.strip() for g in genre_data.split(',')]

q1_games['genres_list'] = q1_games['genres'].apply(clean_genres)
q1_genres = q1_games.explode('genres_list')

# 4. 장르 빈도 분석 및 레드오션(흔한 장르) 제외
genre_counts = q1_genres['genres_list'].value_counts()

# 성공 게임군 내에서 상위 5%에 드는 너무 흔한 장르는 레드오션으로 간주하여 제외
threshold = genre_counts.quantile(0.95)
blue_ocean_genres = genre_counts[genre_counts <= threshold].reset_index()
blue_ocean_genres.columns = ['Genre', 'Count']

# 5. 결과 출력
st.subheader("발굴된 블루오션 장르 (성공군 내 희소 장르)")
st.dataframe(blue_ocean_genres.sort_values(by='Count', ascending=False), use_container_width=True)
