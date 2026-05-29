# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(
    page_title="날짜별 기온분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 날짜별 기온분석")
st.markdown(
    "월과 일을 선택하면 연도별 최고/최저기온과 미래 기온 예측을 확인할 수 있어요!"
)

# ---------------------------
# 데이터 불러오기
# ---------------------------
@st.cache_data
def load_data():

    # 인코딩 예외 처리
    try:
        df = pd.read_csv(
            "seoul.csv",
            encoding="euc-kr"
        )
    except:
        df = pd.read_csv(
            "seoul.csv",
            encoding="utf-8"
        )

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 날짜 오류 제거
    df = df.dropna(subset=["날짜"])

    # 숫자형 변환
    df["최고기온(℃)"] = pd.to_numeric(
        df["최고기온(℃)"],
        errors="coerce"
    )

    df["최저기온(℃)"] = pd.to_numeric(
        df["최저기온(℃)"],
        errors="coerce"
    )

    # 결측치 제거
    df = df.dropna(
        subset=[
            "최고기온(℃)",
            "최저기온(℃)"
        ]
    )

    # 연/월/일 생성
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# ---------------------------
# 사용자 입력
# ---------------------------
col1, col2, col3 = st.columns(3)

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

with col3:
    future_year = st.number_input(
        "🔮 미래 연도 선택",
        min_value=int(df["연도"].max() + 1),
        max_value=2100,
        value=2030
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
# 예측용 데이터
# ---------------------------
X = filtered_df[["연도"]]

# 최고기온 예측
y_max = filtered_df["최고기온(℃)"]

model_max = LinearRegression()
model_max.fit(X, y_max)

pred_max = model_max.predict(
    [[future_year]]
)[0]

# 최저기온 예측
y_min = filtered_df["최저기온(℃)"]

model_min = LinearRegression()
model_min.fit(X, y_min)

pred_min = model_min.predict(
    [[future_year]]
)[0]

# ---------------------------
# 예측 데이터 추가
# ---------------------------
prediction_df = pd.DataFrame({
    "연도": [future_year],
    "최고기온(℃)": [pred_max],
    "최저기온(℃)": [pred_min]
})

graph_df = pd.concat(
    [filtered_df, prediction_df],
    ignore_index=True
)

# ---------------------------
# 그래프 생성
# ---------------------------
fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=graph_df["연도"],
        y=graph_df["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(
            color="hotpink",
            width=4
        ),
        marker=dict(size=8),

        hovertemplate=
        "<b>연도:</b> %{x}<br>" +
        "<b>최고기온:</b> %{y:.1f}℃<extra></extra>"
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=graph_df["연도"],
        y=graph_df["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(
            color="lightblue",
            width=4
        ),
        marker=dict(size=8),

        hovertemplate=
        "<b>연도:</b> %{x}<br>" +
        "<b>최저기온:</b> %{y:.1f}℃<extra></extra>"
    )
)

# ---------------------------
# 레이아웃
# ---------------------------
fig.update_layout(
    title=f"{selected_month}월 {selected_day}일 날짜별 기온분석",
    xaxis_title="연도",
    yaxis_title="온도(℃)",
    template="plotly_white",
    hovermode="x unified",
    legend_title="범례",
    height=700
)

# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------
# 미래 예측 결과
# ---------------------------
st.subheader("🔮 미래 기온 예측")

col4, col5 = st.columns(2)

with col4:
    st.metric(
        f"{future_year}년 예상 최고기온",
        f"{pred_max:.1f}℃"
    )

with col5:
    st.metric(
        f"{future_year}년 예상 최저기온",
        f"{pred_min:.1f}℃"
    )

# ---------------------------
# 데이터 테이블
# ---------------------------
st.subheader("📊 데이터 보기")

st.dataframe(
    graph_df[
        ["연도", "최고기온(℃)", "최저기온(℃)"]
    ],
    use_container_width=True
)
