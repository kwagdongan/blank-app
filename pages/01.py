import streamlit as st
import pandas as pd




# 4. 평가 많은 순 상위 10개 추출
top10_games = df.nlargest(10, 'total_reviews')[['name', 'total_reviews']]

st.dataframe(top10_games)
