import streamlit as st
import pandas as pd
import ast

st.title("진정한 블루오션 장르 발굴 (가중치 분석)")

# 1. 데이터 로드 및 전처리
df = st.session_state['df'].copy()
df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
df['positive_percentual'] = pd.to_numeric(df['positive_percentual'], errors='coerce')
df = df[(df['total_reviews'] > 0) & (df['positive_percentual'] > 0)].copy()

def clean_genres(genre_data):
    if pd.isna(genre_data) or genre_data == '': return []
    if isinstance(genre_data, str) and genre_data.startswith('['):
        try: return ast.literal_eval(genre_data)
        except: return [g.strip() for g in genre_data.replace('[', '').replace(']', '').replace("'", "").split(',')]
    return [g.strip() for g in genre_data.split(',')]

df['genres_list'] = df['genres'].apply(clean_genres)

# 2. 전체 시장의 장르 분포 계산 (Baseline)
all_genres = df.explode('genres_list')
total_counts = all_genres['genres_list'].value_counts(normalize=True) # 비율로 계산

# 3. 제1사분면(성공군) 장르 분포 계산
review_q3 = df['total_reviews'].quantile(0.75)
positive_q3 = df['positive_percentual'].quantile(0.75)
q1_games = df[(df['total_reviews'] >= review_q3) & (df['positive_percentual'] >= positive_q3)].copy()

q1_genres = q1_games.explode('genres_list')
q1_counts = q1_genres['genres_list'].value_counts(normalize=True)

# 4. [핵심] 성공군 장르 가치 점수화
# 공식: (성공군 내 장르 점유율) / (전체 시장 내 장르 점유율)
# 이 값이 1보다 크면 시장 대비 성공한 게임에 더 자주 등장한다는 뜻입니다.
comparison = pd.DataFrame({'Total_Ratio': total_counts, 'Success_Ratio': q1_counts})
comparison['Score'] = comparison['Success_Ratio'] / comparison['Total_Ratio']

# 5. 결과 필터링 (너무 적게 등장하는 데이터는 제외)
min_occurrence = 5 # 최소 5번 이상 등장한 장르만
final_result = comparison[comparison['Score'] > 1].dropna().sort_values(by='Score', ascending=False)

st.subheader("시장 대비 성공률이 높은 블루오션 장르")
st.dataframe(final_result, use_container_width=True)
