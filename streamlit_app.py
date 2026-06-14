import streamlit as st
import pandas as pd
import ast

st.set_page_config(page_title="Steam 분석", layout="wide")


st.title("Steam 데이터 기반 게임 시장 블루오션 장르 분석")

st.markdown("---")

st.header("연구 배경")

st.markdown("""
Steam에는 수만 개의 게임이 등록되어 있으며 다양한 장르가 경쟁하고 있다.

그러나 모든 장르가 동일한 수준의 경쟁과 성과를 보이는 것은 아니다.

일부 장르는 많은 게임이 출시되는 레드오션 시장을 형성하는 반면,
상대적으로 경쟁이 적으면서도 높은 성과를 보이는 장르도 존재한다.
""")

st.header("연구 목적")

st.markdown("""
본 분석의 목적은 Steam 게임 데이터를 활용하여

- 경쟁이 과도하게 집중된 장르를 식별하고
- 높은 평가를 받는 장르를 분석하며
- 상대적으로 경쟁이 적은 블루오션 장르를 탐색하는 것이다.
""")

st.header("연구 질문")

st.markdown("""
1. 가장 경쟁이 치열한 레드오션 태그는 무엇인가?
2. 어떤 태그가 높은 평가를 받는가?
3. 어떤 태그가 낮은 평가를 받는가?
4. 어떤 장르가 블루오션 후보로 볼 수 있는가?
""")









EXCLUDED_TAGS = {"Indie", "Early Access", "Free To Play", "Software Training", "Game Development", "Audio Production", "Utilities","Photo Editing", "Video Production", "Design & Illustration", "Sexual Content", "Nudity", "Animation & Modeling" }


@st.cache_data
def load_data():
    return pd.read_csv('datas.csv', encoding='utf-8-sig')

# 세션에 데이터가 없으면 로드해서 저장
if 'df' not in st.session_state:
    st.session_state['df'] = load_data()




def load_and_clean_data():
    df = pd.read_csv('datas.csv', encoding='utf-8-sig')
    # 1. total_reviews를 숫자로 강제 변환
    # errors='coerce'를 쓰면 숫자로 바꿀 수 없는 값은 자동으로 NaN(결측치)으로 변합니다.
    df['total_reviews'] = pd.to_numeric(df['total_reviews'], errors='coerce')
    
    # 2. total_reviews가 NaN인 행(숫자가 아니었던 행들)은 아예 삭제합니다.
    df_cleaned = df.dropna(subset=['total_reviews'])
    
    return df_cleaned

# 데이터 로드
df = load_and_clean_data()



def clean_genres(genre_data):
    if pd.isna(genre_data) or genre_data == '': 
        return []
    
    # 문자열 처리
    if isinstance(genre_data, str):
        if genre_data.startswith('['):
            try:
                # 리스트 형태의 문자열 처리
                data = ast.literal_eval(genre_data)
            except:
                # 실패 시 쉼표로 분리
                clean = genre_data.replace('[', '').replace(']', '').replace("'", "").replace('"', '')
                data = clean.split(',')
        else:
            data = genre_data.split(',')
    elif isinstance(genre_data, list):
        data = genre_data
    else:
        return []
    
    # [핵심] 리스트 안에서 공백 제거 + 제외 키워드 삭제
    return [g.strip() for g in data if g.strip() != '' and g.strip() not in EXCLUDED_TAGS]


# 덮어쓰기 (중요: 여기서 genres 컬럼 자체를 리스트 값으로 바꿔버림)
df['genres'] = df['genres'].apply(clean_genres)
st.session_state['df'] = df

