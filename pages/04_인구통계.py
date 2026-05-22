import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="경기도 인구통계",
    layout="wide"
)

st.title("📊 경기도의 인구통계")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():

    # 프로젝트 최상위 폴더
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # CSV 경로
    csv_path = os.path.join(BASE_DIR, "population.csv")

    # 파일 존재 확인
    if not os.path.exists(csv_path):
        st.error(f"CSV 파일을 찾을 수 없습니다: {csv_path}")
        st.stop()

    # CSV 읽기
    df = pd.read_csv(csv_path, encoding="euc-kr")

    # 숫자 변환
    age_columns = df.columns[1:]

    for col in age_columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "")
            .astype(int)
        )

    return df

df = load_data()

# -----------------------------
# 행정구 선택
# -----------------------------
region = st.selectbox(
    "🏙️ 행정구를 선택하세요",
    df["행정구"]
)

selected = df[df["행정구"] == region].iloc[0]

ages = df.columns[1:]
population = [selected[col] for col in ages]

# -----------------------------
# 그래프
# -----------------------------
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=ages,
        y=population,
        mode="lines+markers",
        line=dict(
            color="red",
            width=4
        ),
        marker=dict(
            size=8,
            color="red"
        )
    )
)

# -----------------------------
# 디자인
# -----------------------------
fig.update_layout(
    title={
        "text": "경기도의 인구통계",
        "x": 0.5
    },

    xaxis_title="연령대",
    yaxis_title="인구수",

    plot_bgcolor="#E6D5FF",
    paper_bgcolor="#E6D5FF",

    font=dict(
        family="Malgun Gothic",
        size=14,
        color="black"
    ),

    height=600
)

st.plotly_chart(fig, use_container_width=True)
