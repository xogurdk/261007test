import streamlit as st
import datetime
import hashlib

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="오늘의 띠별 운세",
    page_icon="🔮",
    layout="centered"
)

# 2. 12간지 목록 및 데이터 풀 정의
ZODIAC_SIGNS = [
    ("🐭 쥐띠", "쥐띠"),
    ("🐮 소띠", "소띠"),
    ("🐯 호랑이띠", "호랑이띠"),
    ("🐰 토끼띠", "토끼띠"),
    ("🐲 용띠", "용띠"),
    ("🐍 뱀띠", "뱀띠"),
    ("🐴 말띠", "말띠"),
    ("🐑 양띠", "양띠"),
    ("🐵 원숭이띠", "원숭이띠"),
    ("🐔 닭띠", "닭띠"),
    ("🐶 개띠", "개띠"),
    ("🐷 돼지띠", "돼지띠")
]

FORTUNES = [
    {
        "score": "★★★★★",
        "title": "만사형통의 날",
        "desc": "오랫동안 공들인 일에서 기대 이상의 성과를 거둘 수 있습니다. 새로운 도전이나 결정에 자신감을 가져도 좋습니다."
    },
    {
        "score": "★★★★☆",
        "title": "순풍에 돛 단 듯 순조로운 날",
        "desc": "주변 사람들과의 협업이 빛을 발하는 날입니다. 동료나 친구의 조언에 귀를 기울이면 뜻밖의 힌트를 얻습니다."
    },
    {
        "score": "★★★☆☆",
        "title": "평온하고 무난한 하루",
        "desc": "큰 굴곡 없이 일상을 차분하게 정리하기 좋은 날입니다. 서두르기보다 평소 페이스를 유지하는 것이 유리합니다."
    },
    {
        "score": "★★☆☆☆",
        "title": "신중함이 필요한 날",
        "desc": "예상치 못한 변수가 생길 수 있으니 즉흥적인 결정은 피하세요. 말 한마디, 행동 하나에 조금 더 신중을 기하는 편이 좋습니다."
    },
    {
        "score": "★☆☆☆☆",
        "title": "재충전과 휴식이 우선인 날",
        "desc": "무리한 일정보다는 몸과 마음의 에너지를 채우는 데 집중하세요. 오늘은 한 걸음 물러서서 관망하는 지혜가 필요합니다."
    }
]

COLORS = ["화이트", "네이비", "에메랄드 그린", "선셋 오렌지", "스카이 블루", "라벤더", "베이지"]
NUMBERS = [1, 3, 7, 8, 9, 12, 21, 77]
TIPS = [
    "따뜻한 차 한 잔으로 마음의 여유를 챙겨보세요.",
    "주변 사람에게 먼저 가벼운 안부를 전해보세요.",
    "중요한 결정은 내일 아침으로 잠시 미뤄두는 것이 좋습니다.",
    "가벼운 산책이나 스트레칭으로 기분 전환을 시도해보세요.",
    "정리정돈을 통해 주변 환경을 환기해보세요."
]


# 3. 날짜 + 띠 기반 고유 인덱스 생성 함수 (동일 날짜/띠는 하루 동안 결과 유지)
def get_daily_fortune(zodiac_name: str, today_str: str):
    seed_str = f"{today_str}_{zodiac_name}"
    # 해시값을 정수로 변환하여 안정적인 일일 랜덤값 생성
    hash_val = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)

    fortune = FORTUNES[hash_val % len(FORTUNES)]
    color = COLORS[(hash_val // 2) % len(COLORS)]
    number = NUMBERS[(hash_val // 3) % len(NUMBERS)]
    tip = TIPS[(hash_val // 5) % len(TIPS)]

    return fortune, color, number, tip


# 4. UI 구성
st.title("🔮 오늘의 띠별 운세")
today = datetime.date.today()
st.caption(f"기준일: {today.strftime('%Y년 %m월 %d일')}")

st.write("---")

# 띠 선택
selected_label = st.selectbox(
    "본인의 띠를 선택하세요:",
    options=[item[0] for item in ZODIAC_SIGNS],
    index=0
)

# 선택된 순수 띠 이름 추출
sign_name = next(name for label, name in ZODIAC_SIGNS if label == selected_label)

if st.button("운세 확인하기", use_container_width=True, type="primary"):
    fortune, lucky_color, lucky_number, daily_tip = get_daily_fortune(sign_name, str(today))

    st.write("---")
    st.subheader(f"{selected_label} 오늘의 총운")

    # 총운 요약 카드
    st.info(f"**운세 지수:** {fortune['score']} | **{fortune['title']}**\n\n{fortune['desc']}")

    # 상세 행운 정보
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="🎨 행운의 색상", value=lucky_color)
    with col2:
        st.metric(label="🔢 행운의 숫자", value=str(lucky_number))

    st.success(f"💡 **오늘의 실천 팁:** {daily_tip}")