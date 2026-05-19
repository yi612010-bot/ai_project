
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
st.write("📍 서울의 인기 관광지를 한눈에 확인해보세요!")

# 서울 지도 생성
seoul_map = folium.Map(
    location=[37.5665, 126.9780],
    zoom_start=11
)

# 관광지 데이터
places = {
    "경복궁 🏯": {
        "location": [37.579617, 126.977041],
        "station": "경복궁역 (3호선)",
        "description": """
- 조선 시대의 대표 궁궐로 한국 전통문화를 느낄 수 있어요.
- 한복을 입고 사진 찍는 외국인 관광객이 정말 많아요.
- 근처에는 국립민속박물관과 삼청동 카페거리도 있어요.
- 야간개장 시즌에는 아름다운 야경도 즐길 수 있어요.
"""
    },

    "N서울타워 🗼": {
        "location": [37.551169, 126.988227],
        "station": "명동역 (4호선)",
        "description": """
- 서울 야경 명소로 유명한 관광지예요.
- 케이블카를 타고 올라가는 재미가 있어요.
- 사랑의 자물쇠 포토존이 특히 인기예요.
- 밤에는 서울 전체가 내려다보이는 멋진 뷰를 볼 수 있어요.
"""
    },

    "명동 🛍️": {
        "location": [37.563757, 126.985302],
        "station": "명동역 (4호선)",
        "description": """
- 쇼핑과 길거리 음식으로 유명한 핫플레이스예요.
- 화장품 매장과 패션 브랜드가 정말 많아요.
- 떡볶이, 호떡, 닭강정 같은 먹거리가 인기예요.
- 밤에도 사람이 많아 활기찬 분위기를 느낄 수 있어요.
"""
    },

    "북촌한옥마을 🏡": {
        "location": [37.582604, 126.983998],
        "station": "안국역 (3호선)",
        "description": """
- 전통 한옥이 모여 있는 감성적인 관광지예요.
- 골목길마다 예쁜 사진 스팟이 많아요.
- 조용하고 한국적인 분위기를 느끼기 좋아요.
- 근처 삼청동 카페거리도 함께 방문하기 좋아요.
"""
    },

    "홍대 🎵": {
        "location": [37.5563, 126.9220],
        "station": "홍대입구역 (2호선)",
        "description": """
- 젊음과 예술의 거리로 유명한 지역이에요.
- 버스킹 공연과 다양한 맛집이 많아요.
- 감성 카페와 소품샵 구경하는 재미가 있어요.
- 밤에는 클럽과 공연 문화도 활발해요.
"""
    },

    "롯데월드 🎢": {
        "location": [37.5110, 127.0980],
        "station": "잠실역 (2호선)",
        "description": """
- 실내외 놀이공원이 함께 있는 인기 테마파크예요.
- 롤러코스터와 퍼레이드가 특히 유명해요.
- 가족, 친구와 함께 하루 종일 놀기 좋아요.
- 근처 롯데타워와 석촌호수도 함께 즐길 수 있어요.
"""
    },

    "DDP ✨": {
        "location": [37.5665, 127.0092],
        "station": "동대문역사문화공원역",
        "description": """
- 미래형 디자인 건축물로 유명한 랜드마크예요.
- 밤에는 LED 장미정원이 정말 예뻐요.
- 전시회와 패션 행사도 자주 열려요.
- 동대문 쇼핑타운과 함께 구경하기 좋아요.
"""
    },

    "한강공원 🚴": {
        "location": [37.5283, 126.9327],
        "station": "여의나루역 (5호선)",
        "description": """
- 서울 시민들의 대표 힐링 공간이에요.
- 자전거 타기와 피크닉을 즐기기 좋아요.
- 밤에는 한강 야경과 치맥이 유명해요.
- 봄에는 벚꽃 명소로도 인기가 많아요.
"""
    },

    "인사동 🎎": {
        "location": [37.5740, 126.9850],
        "station": "안국역 (3호선)",
        "description": """
- 한국 전통문화와 기념품을 만날 수 있는 거리예요.
- 전통 찻집과 공예품 가게가 많아요.
- 외국인 관광객들이 한글 기념품을 많이 사요.
- 길거리 공연과 전통 먹거리도 즐길 수 있어요.
"""
    },

    "별마당도서관 📚": {
        "location": [37.5125, 127.0589],
        "station": "삼성역 (2호선)",
        "description": """
- 대형 책장으로 유명한 SNS 인기 장소예요.
- 조용하게 책 읽으며 쉬기 좋아요.
- 사진 찍기 좋은 감성 공간으로 유명해요.
- 코엑스몰과 아쿠아리움도 함께 즐길 수 있어요.
"""
    }
}

# 파란색 마커 추가
for name, info in places.items():
    folium.Marker(
        location=info["location"],
        popup=name,
        tooltip=name,
        icon=folium.Icon(
            color="blue",
            icon="info-sign"
        )
    ).add_to(seoul_map)

# 지도 크기 60%로 축소
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    st_folium(seoul_map, width=700, height=500)

# 관광지 선택
st.markdown("---")
st.subheader("🎯 관광지 상세 정보")

selected_place = st.selectbox(
    "궁금한 관광지를 선택하세요 👇",
    list(places.keys())
)

# 선택 정보 출력
info = places[selected_place]

st.markdown(f"## {selected_place}")
st.write(f"🚇 가장 가까운 전철역: {info['station']}")

st.markdown("### 🎡 놀거리 & 특징")
st.write(info["description"])

st.success("🎉 서울 여행 계획 준비 완료!")
