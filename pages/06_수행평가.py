import streamlit as st
import pandas as pd
import plotly.express as px
import json
import requests

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="지역별 성범죄자 수",
    page_icon="🚨",
    layout="wide"
)

st.title("🚨 지역별 성범죄자 수")

# -----------------------------
# 데이터 불러오기
# -----------------------------
data = {
    "시도명": [
        "서울특별시", "부산광역시", "대구광역시", "인천광역시",
        "광주광역시", "대전광역시", "울산광역시", "세종특별자치시",
        "경기도", "강원특별자치도", "충청북도", "충청남도",
        "전북특별자치도", "전라남도", "경상북도", "경상남도",
        "제주특별자치도"
    ],
    "성범죄자수": [
        372, 189, 112, 216,
        100, 73, 45, 6,
        677, 127, 113, 188,
        158, 116, 174, 187,
        48
    ]
}

df = pd.DataFrame(data)

# -----------------------------
# 지역 선택
# -----------------------------
st.sidebar.header("📍 지역 선택")

selected_region = st.sidebar.selectbox(
    "지역을 선택하세요",
    df["시도명"]
)

selected_value = df[df["시도명"] == selected_region]["성범죄자수"].values[0]

st.sidebar.success(
    f"{selected_region}의 성범죄자 수는 {selected_value}명 입니다."
)

# -----------------------------
# 지도용 GeoJSON 불러오기
# -----------------------------
geojson_url = "https://raw.githubusercontent.com/southkorea/southkorea-maps/master/kostat/2013/json/skorea-provinces-2013-geo.json"

geojson = requests.get(geojson_url).json()

# -----------------------------
# 지도 시각화
# -----------------------------
fig = px.choropleth_mapbox(
    df,
    geojson=geojson,
    locations="시도명",
    featureidkey="properties.name",
    color="성범죄자수",
    hover_name="시도명",
    hover_data={
        "성범죄자수": True
    },
    color_continuous_scale="Reds",
    mapbox_style="carto-positron",
    zoom=5.7,
    center={"lat": 36.5, "lon": 127.8},
    opacity=0.8,
    height=750,
)

fig.update_layout(
    title={
        "text": "지역별 성범죄자 수",
        "x": 0.5,
        "xanchor": "center"
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
    x="시도명",
    y="성범죄자수",
    color="성범죄자수",
    color_continuous_scale="Reds",
    title="지역별 성범죄자 수"
)

bar_fig.update_layout(
    xaxis_title="지역",
    yaxis_title="성범죄자 수"
)

st.plotly_chart(bar_fig, use_container_width=True)

# -----------------------------
# 예방 수칙
# -----------------------------
st.markdown("---")

st.subheader("🛡️ 성범죄 예방 수칙")

tips = """
1. 🚶 밤늦게 혼자 다니는 것을 피하기  
2. 📱 위급 상황 시 즉시 112 신고하기  
3. 🔒 문단속과 비밀번호 철저히 관리하기  
4. 👥 사람이 많은 길로 이동하기  
5. 📍 가족이나 친구에게 위치 공유하기  
6. 🚨 위험 상황 발생 시 주변에 도움 요청하기  
"""

st.info(tips)

# -----------------------------
# 출처
# -----------------------------
st.caption("출처: 여성가족부 성범죄자 지역별 집계 현황")
