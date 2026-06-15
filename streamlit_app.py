import streamlit as st
import pandas as pd
import ast

st.set_page_config(page_title="Steam 분석", layout="wide")


st.title("Steam 게임 시장의 장르 경쟁도 및 고성과 장르 분석")

st.markdown("---")


st.header("1. 연구 배경")
st.markdown("""
Steam에는 수만 개의 게임이 등록되어 있으며 매년 새로운 게임이 지속적으로 출시되고 있습니다.

이처럼 경쟁이 심화되는 환경에서는 단순히 인기 장르를 선택하는 것보다,
시장 내 경쟁 수준과 사용자 반응을 함께 고려한 장르 선택이 중요합니다.

따라서 데이터 기반으로 Steam 시장의 구조를 분석하고,
장르별 특성을 파악할 필요가 있습니다.
""")
    
st.header("2. 연구 목적")
st.markdown("""
본 연구의 목적은 Steam 게임 데이터를 분석하여 경쟁이 과도하게 집중된 장르를 식별하고, 
상대적으로 경쟁이 적으면서 높은 평가를 받는 장르를 파악합니다.
파악된 장르는 저를 포함한 게임 개발자들의 추후 게임 개발 정보로 활용됩니다. 
""")


st.header("3. 분석 방법")
st.markdown("""
Steam 게임 데이터의 태그(장르), 리뷰 수, 긍정 평가 비율 수치를 활용하였습니다.

- 리뷰 수와 긍정 평가 비율을 조정해 게임군(고성과 게임군) 식별
- 각 태그에서 고성과 게임을 전체 게임 수로 나누어 태그별 고성과 게임 비중 산출
- 태그별 게임 출시 수를 통해 시장 내 경쟁 밀도 산출
- 태그별 경쟁 밀도와 태그별 고성과 게임 비중을 이용하여 블루오션 후보 태그 식별
""")
    

st.markdown("---")


st.subheader("데이터 출처 및 라이선스")
st.info("""
본 분석은 **Valve Corporation**에서 제공하는 **Steam Web API**를 활용하였습니다.
- 데이터 출처: Steam Web API (https://partner.steamgames.com/doc/webapi)
""")







EXCLUDED_TAGS = {
    "Indie", "Early Access", "Free To Play", "Software Training", 
    "Game Development", "Audio Production", "Utilities", "Photo Editing", 
    "Video Production", "Design & Illustration", "Sexual Content", 
    "Nudity", "Animation & Modeling", "Web Publishing"
}

# 0부터 100까지의 숫자를 문자열로 변환하여 추가
numbers_to_add = {str(i) for i in range(101)}

# 기존 집합(set)에 업데이트
EXCLUDED_TAGS.update(numbers_to_add)




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
df = df.nlargest(10000, 'total_reviews')
st.session_state['df'] = df

