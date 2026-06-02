import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="지역별 성범죄자 수",
    page_icon="🚨",
    layout="wide"
)

# -----------------------------
# 제목
# -----------------------------
st.title("🚨 지역별 성범죄자 수")

# -----------------------------
# 데이터
# -----------------------------
df = pd.DataFrame({
    "지역": [
        "서울", "부산", "대구", "인천",
        "광주", "대전", "울산", "세종",
        "경기", "강원", "충북", "충남",
        "전북", "전남", "경북", "경남",
        "제주"
    ],
    "성범죄자수": [
        372, 189, 112, 216,
        100, 73, 45, 6,
        677, 127, 113, 188,
        158, 116, 174, 187,
        48
    ],
    "위도": [
        37.5665, 35.1796, 35.8714, 37.4563,
        35.1595, 36.3504, 35.5384, 36.4800,
        37.4138, 37.8228, 36.6357, 36.5184,
        35.7175, 34.8679, 36.4919, 35.4606,
        33.4996
    ],
    "경도": [
        126.9780, 129.0756, 128.6014, 126.7052,
        126.8526, 127.3845, 129.3114, 127.2890,
        127.5183, 128.1555, 127.4914, 126.8000,
        127.1530, 126.9910, 128.8889, 128.2132,
        126.5312
    ]
})

# -----------------------------
# 사이드바
# -----------------------------
st.sidebar.header("📍 지역 선택")

selected_region = st.sidebar.selectbox(
    "지역을 선택하세요",
    df["지역"]
)

selected_value = df[df["지역"] == selected_region]["성범죄자수"].values[0]

st.sidebar.success(
    f"{selected_region}의 성범죄자 수는 {selected_value}명 입니다."
)

# -----------------------------
# 지도 시각화
# -----------------------------
fig = px.scatter_mapbox(
    df,
    lat="위도",
    lon="경도",
    size="성범죄자수",
    color="성범죄자수",
    hover_name="지역",
    hover_data={
        "성범죄자수": True,
        "위도": False,
        "경도": False
    },
    color_continuous_scale="Reds",
    zoom=5.5,
    center={"lat": 36.5, "lon": 127.8},
    height=800,
    size_max=40
)

fig.update_layout(
    mapbox_style="carto-positron",
    title={
        "text": "지역별 성범죄자 수",
        "x": 0.5
    },
    margin={"r":0,"t":60,"l":0,"b":0},
    coloraxis_colorbar=dict(
        title="성범죄자 수"
    )
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 막대 그래프
# -----------------------------
st.subheader("📊 지역별 비교")

bar_fig = px.bar(
    df.sort_values("성범죄자수", ascending=False),
    x="지역",
    y="성범죄자수",
    color="성범죄자수",
    color_continuous_scale="Reds",
    title="지역별 성범죄자 수"
)

st.plotly_chart(bar_fig, use_container_width=True)

# -----------------------------
# 예방수칙
# -----------------------------
st.markdown("---")

st.subheader("🛡️ 성범죄 예방수칙")

st.info("""
1. 🚶 늦은 밤 혼자 다니지 않기  
2. 📱 위급 시 112 신고하기  
3. 🔒 출입문 잠금 확인하기  
4. 👥 사람이 많은 길 이용하기  
5. 📍 가족·친구와 위치 공유하기  
6. 🚨 위험하면 즉시 도움 요청하기
""")

# -----------------------------
# 출처
# -----------------------------
st.caption("출처 : 여성가족부")
