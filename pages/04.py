import streamlit as st
import pandas as pd
import ast

st.title("핵심 성공 태그 분석 (제1사분면 전략)")

# 1. 데이터 로드 및 0 초과 정제
df = st.session_state['df'].copy()
df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
df['positive_percentual'] = pd.to_numeric(df['positive_percentual'], errors='coerce')
df = df[(df['total_reviews'] > 0) & (df['positive_percentual'] > 0)].copy()

# 2. 제1사분면(리뷰 상위 25% & 긍정 비율 상위 25%) 정의
review_q3 = df['total_reviews'].quantile(0.75)
positive_q3 = df['positive_percentual'].quantile(0.75)

# 1사분면 게임들만 추출
q1_games = df[(df['total_reviews'] >= review_q3) & (df['positive_percentual'] >= positive_q3)].copy()

st.write(f"📊 제1사분면(성공 게임) 정의: 리뷰 {review_q3:.0f}개 이상 & 긍정 비율 {positive_q3:.1f}% 이상")
st.write(f"분석 대상 성공 게임 수: {len(q1_games)}개")

# 3. 태그 데이터 정제 및 분리
def clean_tags(tag_data):
    if pd.isna(tag_data) or tag_data == '': return []
    if isinstance(tag_data, str) and tag_data.startswith('['):
        try: return ast.literal_eval(tag_data)
        except: return [t.strip() for t in tag_data.replace('[', '').replace(']', '').replace("'", "").split(',')]
    return [t.strip() for t in tag_data.split(',')]

q1_games['tags_list'] = q1_games['tags'].apply(clean_tags)
q1_tags = q1_games.explode('tags_list')

# 4. 태그 빈도 분석 및 레드오션(너무 흔한 태그) 제외
tag_counts = q1_tags['tags_list'].value_counts()

# 레드오션 기준: 제1사분면 내에서 등장 빈도가 상위 5%인 태그는 '너무 흔함'으로 간주
threshold = tag_counts.quantile(0.95)
blue_ocean_tags = tag_counts[tag_counts <= threshold].reset_index()
blue_ocean_tags.columns = ['Tag', 'Count']

# 5. 결과 출력
st.subheader("발굴된 블루오션 태그 (성공 게임군 내 희소 태그)")
st.dataframe(blue_ocean_tags.sort_values(by='Count', ascending=False), use_container_width=True)

st.info("💡 해석: 위 태그들은 성공한 게임(제1사분면)들에는 포함되어 있지만, 너무 흔하지는 않은 '가치 있는 특징'들입니다.")
