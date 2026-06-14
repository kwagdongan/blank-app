import streamlit as st
import pandas as pd
import ast

st.title("진정한 블루오션 장르 발굴 (상위 5개 제외)")

# 1. 데이터 로드 및 정제
df = st.session_state['df']

df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
df['positive_percentual'] = pd.to_numeric(df['positive_percentual'], errors='coerce')
df = df[(df['total_reviews'] > 0) & (df['positive_percentual'] > 0)].copy()


# 2. [확정] 전체 시장 기준 레드오션 Top 5 추출
all_genres_exploded = df.explode('genres')
red_ocean_top5 = all_genres_exploded['genres'].value_counts().nlargest(5).index.tolist()

st.write(f"🛑 **레드오션으로 분류되어 제외된 장르(Top 5):** {', '.join(red_ocean_top5)}")

# 3. 제1사분면(성공군) 데이터 추출
review_q3 = df['total_reviews'].quantile(0.75)
positive_q3 = df['positive_percentual'].quantile(0.75)
q1_games = df[(df['total_reviews'] >= review_q3) & (df['positive_percentual'] >= positive_q3)].copy()

# 4. 성공군 데이터에서 레드오션 장르를 제외한 장르만 필터링
q1_genres_exploded = q1_games.explode('genres')
blue_ocean_candidates = q1_genres_exploded[~q1_genres_exploded['genres'].isin(red_ocean_top5)]

# 5. 빈도수 및 평균 긍정 비율 계산 (결과 정렬)
result = blue_ocean_candidates.groupby('genres').agg(
    성공_게임수=('name', 'count'),
    평균_긍정비율=('positive_percentual', 'mean')
).sort_values(by='성공_게임수', ascending=False)

# 6. 결과 출력
st.subheader("발굴된 블루오션 장르 (레드오션 Top 5 제외)")
st.dataframe(result, use_container_width=True)

st.write("💡 **해석:** 위 장르들은 가장 대중적인 5개 장르에 속하지 않으면서, 동시에 성공한 게임군에서 자주 발견되는 가치 있는 장르들입니다.")
