import streamlit as st
import pandas as pd
import ast

st.set_page_config(page_title="Steam 분석", layout="wide")


st.title("Steam 데이터 기반 게임 시장 블루오션 장르 분석")

st.markdown("---")

# 레이아웃을 크게 좌우로 나눕니다.
col1, col2 = st.columns(2)

# 왼쪽 열: 연구 배경과 목적 (1, 2번)
with col1:
    st.header("1. 연구 배경")
    st.markdown("""
    Steam에는 수만 개의 게임이 등록되어 있으며 다양한 장르가 경쟁하고 있습니다.
    일부 장르는 높은 경쟁률을 보이는 레드오션인 반면, 
    상대적으로 경쟁이 적으면서도 높은 사용자 평가를 받는 장르도 존재합니다. 
    본 연구는 Steam 데이터를 활용하여 시장의 경쟁 정도와 사용자 반응을 분석하고, 
    전략적으로 유효한 장르를 탐색하는 데 목적이 있습니다.
    """)
    
    st.header("2. 연구 목적")
    st.markdown("""
    본 연구의 목적은 Steam 게임 데이터를 분석하여 경쟁이 과도하게 집중된 장르를 식별하고, 
    상대적으로 경쟁이 적으면서 높은 평가를 받는 장르의 핵심 특성을 파악하는 것입니다. 
    """)

# 오른쪽 열: 분석 방법과 연구 질문 (3, 4번)
with col2:
    st.header("3. 분석 방법")
    st.markdown("""
    Steam 게임 데이터의 태그, 리뷰 수, 긍정 평가 비율을 종합적으로 활용하였습니다.
    - **경쟁 분석:** 태그별 게임 출시 수를 통해 시장 내 경쟁 밀도 측정
    - **성과 분석:** 태그별 평균 긍정 평가 비율을 통한 사용자 만족도 산출
    - **고성과군 정의:** 리뷰 수와 긍정 평가 비율이 모두 높은 게임군 식별
    - **전략적 탐색:** 레드오션 장르를 제외한 고성과군 태그를 추출하여 블루오션 영역 도출
    """)
    
    st.header("4. 연구 질문")
    st.markdown("""
    1. Steam 생태계 내에서 가장 점유율이 높은 장르는 무엇인가?
    2. 사용자 만족도가 가장 높은 장르와 낮은 장르는 각각 무엇인가?
    3. 게임 출시 수가 과도하게 집중되어 경쟁이 치열한 레드오션 장르는 무엇인가?
    4. 낮은 경쟁률 대비 높은 성과를 보이는 블루오션 장르는 무엇인가?
    """)

st.markdown("---")

# 데이터 출처 섹션: 좀 더 격식 있게 구성
st.subheader("데이터 출처 및 라이선스")
st.info("""
본 분석은 **Valve Corporation**에서 제공하는 **Steam Web API**를 활용하였습니다.
- 데이터 출처: Steam Web API (https://partner.steamgames.com/doc/webapi)
- 데이터 수집 시점: 2026년 6월
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

