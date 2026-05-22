import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="경기도 인구통계",
    layout="wide"
)

# -----------------------------
# 제목
# -----------------------------
st.title("📊 경기도의 인구통계")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="euc-kr")

    # 숫자 컬럼 변환
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

# 선택 데이터
selected = df[df["행정구"] == region].iloc[0]

# 연령대 / 인구수
ages = df.columns[1:]
population = [selected[col] for col in ages]

# -----------------------------
# Plotly 그래프
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
# 그래프 디자인
# -----------------------------
fig.update_layout(
    title={
        "text": "경기도의 인구통계",
        "x": 0.5,
        "xanchor": "center"
    },

    xaxis_title="연령대",
    yaxis_title="인구수",

    plot_bgcolor="#EBDCFF",   # 연한 보라색
    paper_bgcolor="#EBDCFF",

    font=dict(
        family="Malgun Gothic",
        size=14,
        color="black"
    ),

    height=600
)

# 축 스타일
fig.update_xaxes(
    showgrid=True,
    gridcolor="white"
)

fig.update_yaxes(
    showgrid=True,
    gridcolor="white"
)

# -----------------------------
# 출력
# -----------------------------
st.plotly_chart(
    fig,
    use_container_width=True
)
