# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="날짜별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 날짜별 기온분석")
st.markdown("월과 일을 선택하면 연도별 최고/최저기온을 확인할 수 있어요!")

# ---------------------------
# 데이터 불러오기
# ---------------------------
@st.cache_data
def load_data():

    # 인코딩 오류 대비
    try:
        df = pd.read_csv("seoul.csv", encoding="euc-kr")
    except:
        df = pd.read_csv("seoul.csv", encoding="utf-8")

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 잘못된 날짜 제거
    df = df.dropna(subset=["날짜"])

    # 연/월/일 컬럼 생성
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# ---------------------------
# 월 / 일 선택
# ---------------------------
col1, col2 = st.columns(2)

with col1:
    selected_month = st.selectbox(
        "📅 월 선택",
        sorted(df["월"].unique())
    )

with col2:
    selected_day = st.selectbox(
        "📌 일 선택",
        sorted(
            df[df["월"] == selected_month]["일"].unique()
        )
    )

# ---------------------------
# 데이터 필터링
# ---------------------------
filtered_df = df[
    (df["월"] == selected_month) &
    (df["일"] == selected_day)
]

filtered_df = filtered_df.sort_values("연도")

# ---------------------------
# 그래프 생성
# ---------------------------
fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(
            color="hotpink",
            width=4
        )
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(
            color="lightblue",
            width=4
        )
    )
)

# 레이아웃
fig.update_layout(
    title=f"{selected_month}월 {selected_day}일 날짜별 기온분석",
    xaxis_title="연도",
    yaxis_title="온도(℃)",
    template="plotly_white",
    hovermode="x unified",
    legend_title="범례",
    height=650
)

# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------
# 데이터 테이블
# ---------------------------
st.subheader("📊 선택한 날짜 데이터")

st.dataframe(
    filtered_df[
        ["연도", "최고기온(℃)", "최저기온(℃)"]
    ],
    use_container_width=True
)
