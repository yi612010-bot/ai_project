import streamlit as st
from streamlit_folium import st_folium
import folium

# 페이지 설정
st.set_page_config(
    page_title="서울 관광지 TOP10",
    page_icon="🌏",
    layout="wide"
)

# 제목
st.title("🌏 외국인들이 좋아하는 서울 관광지 TOP10")
st.write("📍 Folium 지도로 서울의 인기 관광지를 확인해보세요!")

# 서울 중심 좌표
seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11
)

# 관광지 데이터
places = [
    {
        "name": "경복궁 🏯",
        "location": [37.579617, 126.977041],
        "description": "조선 시대 대표 궁궐"
    },
    {
        "name": "N서울타워 🗼",
        "location": [37.551169, 126.988227],
        "description": "서울 야경 명소"
    },
    {
        "name": "명동 🛍️",
        "location": [37.563757, 126.985302],
        "description": "쇼핑 천국"
    },
    {
        "name": "북촌한옥마을 🏡",
        "location": [37.582604, 126.983998],
        "description": "전통 한옥 마을"
    },
    {
        "name": "홍대 🎵",
        "location": [37.5563, 126.9220],
        "description": "젊음과 예술의 거리"
    },
    {
        "name": "롯데월드 🎢",
        "location": [37.5110, 127.0980],
        "description": "인기 테마파크"
    },
    {
        "name": "DDP ✨",
        "location": [37.5665, 127.0092],
        "description": "디자인 랜드마크"
    },
    {
        "name": "한강공원 🚴",
        "location": [37.5283, 126.9327],
        "description": "서울 대표 힐링 공간"
    },
    {
        "name": "인사동 🎎",
        "location": [37.5740, 126.9850],
        "description": "전통 문화 거리"
    },
    {
        "name": "별마당도서관 📚",
        "location": [37.5125, 127.0589],
        "description": "SNS 인기 명소"
    }
]

# 마커 추가
for place in places:
    folium.Marker(
        location=place["location"],
        popup=f"{place['name']}<br>{place['description']}",
        tooltip=place["name"]
    ).add_to(seoul_map)

# 지도 출력
st_folium(seoul_map, width=1000, height=600)

# 리스트 출력
st.markdown("---")
st.subheader("🏆 관광지 리스트")

for i, place in enumerate(places, start=1):
    st.write(f"{i}. {place['name']} - {place['description']}")

st.success("🎉 Streamlit Cloud 배포 성공!")
