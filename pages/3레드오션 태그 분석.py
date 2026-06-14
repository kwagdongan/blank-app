import streamlit as st
import pandas as pd
import altair as alt

st.title("레드오션 태그 분석")

df = st.session_state['df']

# 태그 펼치기
df_genres = df.explode('genres')

# 빈도 계산
genre_counts = df_genres['genres'].value_counts().reset_index()
genre_counts.columns = ['태그', '빈도']
genre_counts = genre_counts[genre_counts['태그'] != '']

# 상위 8%
q92 = genre_counts['빈도'].quantile(0.1)
top_group = genre_counts[genre_counts['빈도'] >= q92]

# 전체 평균
overall_avg = genre_counts['빈도'].mean()

st.subheader("태그 빈도 상위 그룹")

st.dataframe(
    top_group,
    use_container_width=True,
    hide_index=True
)

# 막대그래프
bars = alt.Chart(top_group).mark_bar().encode(
    x=alt.X(
        '빈도:Q',
        title='등장 빈도'
    ),
    y=alt.Y(
        '태그:N',
        sort='-x',
        title=None
    )
)

# 평균선
avg_line = alt.Chart(
    pd.DataFrame({'평균': [overall_avg]})
).mark_rule().encode(
    x='평균:Q'
)

chart = (
    bars + avg_line
).properties(
    height=400
)

st.altair_chart(
    chart,
    use_container_width=True
)

st.caption(
    f"선은 전체 태그 평균 빈도를 의미함.({overall_avg:.1f})"
)





q1 = genre_counts['빈도'].quantile(0.25)
q3 = genre_counts['빈도'].quantile(0.75)

iqr = q3 - q1

threshold = q3 + 1.5 * iqr

red_ocean_tags = genre_counts[
    genre_counts['빈도'] >= threshold
]['태그'].tolist()

st.markdown("---")

st.subheader("레드오션 태그 정의")

st.write(
    f"""
    태그 빈도 분포의 사분위수(IQR)를 이용하여 레드오션 태그를 정의하였다.

    - 제1사분위수(Q1): {q1:.1f}
    - 제3사분위수(Q3): {q3:.1f}
    - IQR: {iqr:.1f}
    - 기준값(Q3 + 1.5×IQR): {threshold:.1f}

    본 연구에서는 기준값을 초과하는 태그를 레드오션 태그로 분류하였다.
    """
)

st.success(
    f"레드오션 태그: {', '.join(red_ocean_tags)}"
)
