# app.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="🌍 MBTI World Dashboard",
    page_icon="🧠",
    layout="wide"
)

# -----------------------------
# 제목
# -----------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #ff4b4b;'>
    🌍 세계 국가별 MBTI 분석 대시보드
    </h1>
    <p style='text-align: center; font-size:18px;'>
    국가를 선택하면 MBTI 비율을 인터랙티브하게 확인할 수 있어요 ✨
    </p>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# -----------------------------
# MBTI 컬럼 추출
# -----------------------------
mbti_cols = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
]

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.header("⚙️ 설정")

selected_country = st.sidebar.selectbox(
    "🌎 국가 선택",
    df["Country"].unique()
)

# -----------------------------
# 선택된 국가 데이터
# -----------------------------
country_data = df[df["Country"] == selected_country].iloc[0]

mbti_values = [country_data[col] * 100 for col in mbti_cols]

plot_df = pd.DataFrame({
    "MBTI": mbti_cols,
    "비율": mbti_values
})

# -----------------------------
# 가장 높은 MBTI 찾기
# -----------------------------
top_mbti = plot_df.loc[plot_df["비율"].idxmax(), "MBTI"]

# -----------------------------
# 색상 설정
# 1등 = 빨간색
# 나머지 = 파란색 그라데이션
# -----------------------------
colors = []

blue_scale = px.colors.sequential.Blues

sorted_df = plot_df.sort_values("비율", ascending=False)

for idx, row in sorted_df.iterrows():
    if row["MBTI"] == top_mbti:
        colors.append("#ff2b2b")
    else:
        scale_index = min(len(colors), len(blue_scale)-1)
        colors.append(blue_scale[scale_index])

sorted_df["color"] = colors

# -----------------------------
# 메인 화면
# -----------------------------
col1, col2 = st.columns([2,1])

with col1:

    st.subheader(f"📊 {selected_country} MBTI 비율 분석")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=sorted_df["MBTI"],
            y=sorted_df["비율"],
            marker_color=sorted_df["color"],
            text=[f"{v:.1f}%" for v in sorted_df["비율"]],
            textposition="outside",
            hovertemplate=
            "<b>%{x}</b><br>" +
            "비율: %{y:.2f}%<extra></extra>"
        )
    )

    fig.update_layout(
        height=600,
        template="plotly_white",
        xaxis_title="MBTI 유형",
        yaxis_title="비율 (%)",
        title={
            "text": f"🧠 {selected_country} MBTI 분포",
            "x": 0.5,
            "xanchor": "center"
        },
        font=dict(size=15),
        hoverlabel=dict(
            bgcolor="white",
            font_size=14
        )
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("🏆 가장 높은 MBTI")

    top_value = sorted_df.iloc[0]["비율"]

    st.markdown(
        f"""
        <div style="
            background-color:#fff5f5;
            padding:25px;
            border-radius:20px;
            text-align:center;
            border:2px solid #ff4b4b;
        ">
            <h1 style="color:#ff2b2b;">{top_mbti}</h1>
            <h2>{top_value:.1f}%</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### 📌 특징")

    descriptions = {
        "INTJ": "전략적이고 독립적인 성향 🧠",
        "INTP": "논리와 분석을 좋아함 🔍",
        "ENTJ": "리더십과 추진력이 강함 🚀",
        "ENTP": "창의적이고 토론을 즐김 💡",
        "INFJ": "이상주의적이고 통찰력이 깊음 🌙",
        "INFP": "감성적이고 공감 능력이 뛰어남 💖",
        "ENFJ": "사람들을 이끄는 따뜻한 리더 🤝",
        "ENFP": "열정적이고 자유로운 분위기 ✨",
        "ISTJ": "책임감 있고 체계적 📚",
        "ISFJ": "배려심 많고 성실함 🌷",
        "ESTJ": "현실적이고 조직적 📊",
        "ESFJ": "친화력 좋고 사교적 😊",
        "ISTP": "실용적이고 문제 해결 능력 우수 🔧",
        "ISFP": "예술 감각과 감성이 풍부 🎨",
        "ESTP": "활동적이고 에너지가 넘침 ⚡",
        "ESFP": "분위기 메이커 🎉"
    }

    st.info(descriptions[top_mbti])

# -----------------------------
# 하단 테이블
# -----------------------------
st.markdown("---")

st.subheader("📋 MBTI 비율 데이터")

styled_df = sorted_df.copy()
styled_df["비율"] = styled_df["비율"].map(lambda x: f"{x:.2f}%")

st.dataframe(
    styled_df[["MBTI", "비율"]],
    use_container_width=True,
    hide_index=True
)
