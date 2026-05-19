# 📌 Streamlit + Folium 서울 관광지 TOP10 프로젝트

## 📁 app.py

```python
import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(
    page_title="🌏 서울 관광지 TOP10",
    page_icon="📍",
    layout="wide"
)

st.title("🌏 외국인들이 좋아하는 서울 관광지 TOP10")
st.write("📍 Folium 지도로 서울의 인기 관광지를 확인해보세요!")

# 서울 중심 좌표
seoul_map = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

# 관광지 데이터
places = [
    {
        "name": "경복궁 🏯",
        "location": [37.579617, 126.977041],
        "description": "조선 시대의 대표 궁궐"
    },
    {
        "name": "N서울타워 🗼",
        "location": [37.551169, 126.988227],
        "description": "서울 야경 명소"
    },
    {
        "name": "명동 🛍️",
        "location": [37.563757, 126.985302],
        "description": "쇼핑과 먹거리의 중심지"
    },
    {
        "name": "북촌한옥마을 🏡",
        "location": [37.582604, 126.983998],
        "description": "전통 한옥이 모여 있는 마을"
    },
    {
        "name": "홍대 🎵",
        "location": [37.5563, 126.9220],
        "description": "젊음과 예술의 거리"
    },
    {
        "name": "롯데월드 🎢",
        "location": [37.5110, 127.0980],
        "description": "대형 테마파크"
    },
    {
        "name": "동대문디자인플라자(DDP) ✨",
        "location": [37.5665, 127.0092],
        "description": "미래형 건축 랜드마크"
    },
    {
        "name": "한강공원 🚴",
        "location": [37.5283, 126.9327],
        "description": "서울 시민들의 힐링 공간"
    },
    {
        "name": "인사동 🎎",
        "location": [37.5740, 126.9850],
        "description": "전통 문화 거리"
    },
    {
        "name": "코엑스 별마당도서관 📚",
        "location": [37.5125, 127.0589],
        "description": "SNS 인기 포토존"
    }
]

# 마커 추가
for place in places:
    folium.Marker(
        location=place["location"],
        popup=f"<b>{place['name']}</b><br>{place['description']}",
        tooltip=place["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(seoul_map)

# 지도 출력
st_folium(seoul_map, width=1000, height=600)

st.markdown("---")
st.subheader("🏆 서울 관광지 TOP10 리스트")

for idx, place in enumerate(places, start=1):
    st.write(f"{idx}. {place['name']} - {place['description']}")

st.success("🎉 Streamlit Cloud에서 바로 배포 가능!")
```

---

## 📁 requirements.txt

```txt
streamlit
folium
streamlit-folium
```

---

# 🚀 Streamlit Cloud 배포 방법

1. GitHub에 `app.py` 와 `requirements.txt` 업로드
2. Streamlit Cloud 접속
3. GitHub 저장소 연결
4. `app.py` 선택 후 Deploy 클릭
5. 완료 🎉
