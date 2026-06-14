import streamlit as st
import pandas as pd
import ast

st.set_page_config(page_title="Steam 분석", layout="wide")


st.title("🎮 Steam 데이터 기반 게임 시장 블루오션 장르 분석")
st.caption("Steam 게임 데이터를 활용하여 경쟁이 적고 성과가 높은 장르를 탐색한다.")

st.markdown("---")

# ======================
# 연구 배경 / 연구 목적
# ======================

col1, col2 = st.columns(2)

with col1:
    st.info("""
    ### 📌 연구 배경

    Steam에는 수만 개의 게임이 등록되어 있으며 다양한 장르가 경쟁하고 있다.

    그러나 모든 장르가 동일한 수준의 경쟁과 성과를 보이는 것은 아니다.

    일부 장르는 많은 게임이 출시되어 경쟁이 치열한 **레드오션 시장**을 형성하는 반면,
    일부 장르는 상대적으로 경쟁이 적으면서도 높은 평가를 받고 있다.

    따라서 Steam 데이터를 활용하여 시장 구조를 분석하고,
    전략적으로 활용 가능한 장르를 탐색할 필요가 있다.
    """)

with col2:
    st.success("""
    ### 🎯 연구 목적

    본 연구는 Steam 게임 데이터를 분석하여

    • 경쟁이 과도하게 집중된 태그 식별

    • 높은 평가를 받는 태그 분석

    • 저평가 태그 분석

    • 블루오션 태그 탐색

    을 수행하는 것을 목적으로 한다.
    """)

st.markdown("---")

# ======================
# 분석 방법
# ======================

st.subheader("⚙️ 분석 방법")

st.markdown("""
본 연구에서는 Steam 게임 데이터의 **태그, 리뷰 수, 긍정 평가 비율**을 활용하였다.
""")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("📊 경쟁도", "태그별 게임 수")

with c2:
    st.metric("👍 만족도", "긍정 평가 비율")

with c3:
    st.metric("🔥 관심도", "총 리뷰 수")

st.markdown("""

분석 절차는 다음과 같다.

1. 태그별 게임 수를 이용하여 경쟁 정도 분석
2. 태그별 평균 긍정 평가 비율 분석
3. 리뷰 수와 긍정 평가 비율이 모두 높은 게임을 **고성과 게임군**으로 정의
4. 경쟁이 높은 **레드오션 태그** 식별
5. 고성과 게임군에서 레드오션 태그를 제외한 후 **블루오션 태그 탐색**
""")

st.markdown("---")

# ======================
# 연구 질문
# ======================

st.subheader("🔍 연구 질문")

q1, q2 = st.columns(2)

with q1:
    st.info("① Steam에서 가장 많이 사용되는 태그는 무엇인가?")
    st.info("② 어떤 태그가 높은 긍정 평가를 받는가?")

with q2:
    st.info("③ 어떤 태그가 낮은 긍정 평가를 받는가?")
    st.info("④ 블루오션 태그는 무엇인가?")

st.markdown("---")

# ======================
# 데이터 출처
# ======================

with st.expander("📂 데이터 출처"):
    st.markdown("""
    **Steam Web API (Valve Corporation)**

    - 게임 정보
    - 태그 정보
    - 리뷰 정보
    - 평점 정보
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

