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
q92 = genre_counts['빈도'].quantile(0.80)
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





std_freq = genre_counts['빈도'].std()

threshold = overall_avg + std_freq

red_ocean_tags = genre_counts[
    genre_counts['빈도'] >= threshold
]['태그'].tolist()

st.markdown("---")

st.subheader("레드오션 태그 정의")

st.write(
    f"전체 태그 평균 빈도({overall_avg:.1f})와 "
    f"표준편차({std_freq:.1f})를 이용하여 "
    f"평균 + 1표준편차({threshold:.1f}) 이상인 태그를 "
    f"레드오션 태그로 정의하였다."
)

st.success(
    f"레드오션 태그: {', '.join(red_ocean_tags)}"
)
