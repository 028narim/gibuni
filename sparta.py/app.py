import re
import openai
import streamlit as st
import os
import requests
import json
from datetime import datetime, timedelta
import time
import streamlit.components.v1 as components

# ==== 설정 ====
os.environ["OPENAI_API_KEY"] = st.secrets["API_KEY"]
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# ==== 페이지 설정 ====
st.set_page_config(page_title="오늘의 기분", layout="centered")

# ==== 커스텀 CSS ====
st.markdown("""
<style>
    :root {
        --pink-light: #FFF0F7;
        --pink-dark: #E9428E;
        --pink-normal: #F472B6 ;
        --gray-dark: #F3F4F6;
    }

    /* 바깥쪽 전체 배경 */
    .stApp {
        background-color: var(--pink-light);
    }

    /* 메인 영역 흰색 박스 */
    .css-1d391kg {
        background-color: #FFFFFF !important;
        border-radius: 24px;
        padding: 2rem;
        max-width: 800px !important;
        margin: 0 auto;
    }

    h2, h3, .stSubheader {
        color: var(--pink-dark) !important;
    }
    
    h3 {
        font-size: 15px;
    }

    h1 {
        text-align: center;
        color: var(--pink-normal) !important;
    }

    /* 감정 버튼 스타일 */
    .stButton > button {
        background-color: var(--pink-light);
        color: black;
        border: 1.5px solid var(--pink-dark);
        border-radius: 16px;
        height: 120px;
        width: 200px;
        font-size: 2.5rem;
        font-weight: bold;
        transition: all 0.3s;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        line-height: 1.2;
        white-space: pre-line !important;
    }

    .stButton > button:hover {
        background-color: var(--pink-dark);
        color: white;
    }

    .stButton > button:focus {
        background-color: var(--pink-dark);
        color: white !important;
        border: 2px solid var(--pink-dark);
    }

    /* 일정 등록 버튼 */
    div.stButton > button {
        color: var(--pink-dark);
        font-weight: bold;
        height: 50px;
        width: 100%;
        font-size: 16px;
    }

    /* 선택된 감정 박스 */
    .selected-mood-box {
        background-color: #FFF;
        border-radius: 16px;
        padding: 1rem;
        align-items: center;
        justify-content: center;
        margin-top: 1rem;
        font-size: 1rem;
        color: var(--pink-dark);
        font-weight: bold;
        height: 60px;
    }

    /* 입력창 placeholder */
    textarea::placeholder {
        color: #E9428E !important;
        opacity: 1;
    }

    .stTextArea > div > div {
        border-radius: 12px;
        background-color: #FFF;
    }

    /* 경고창 수정 (warning) */
    div[data-testid="stAlert"] {
        background-color: #ffffff !important;
        border: 1px solid #f0f0f0;
        color: #E9428E;
        border-radius: 12px;
    }

    /* 결과 카드 */
     .glass-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        padding: 2rem; /* 넉넉한 패딩 */
        margin-bottom: 1rem; /* 카드 간격 */
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    /* 날짜 텍스트 */
    .date {
        text-align: center;
        color: #6B7280;
        margin: 1rem 0;
    }

    /* 섹션 제목 */
    .subheader {
        color: var(--pink-dark);
        font-size: 1.3rem;
        font-weight: bold;
        margin-top: 2rem;
    }

    /* 안 보이는 버튼 숨기기 */
    button[key^="btn_"] {
        display: none !important;
    }

</style>
""", unsafe_allow_html=True)

# ==== 초기 상태 ====
if "mood" not in st.session_state:
    st.session_state.mood = None
    st.session_state.selected_index = -1

# ==== 타이틀 ====
st.title("🔮 기부니 태도가 되")

st.markdown("""
<div style="text-align:center; font-style:italic; margin-top: 1rem;">
직장인들의 기분을 파악하여 처방해주는 만병통치 서비스 💊
</div>
""", unsafe_allow_html=True)

# ==== 감정 선택 UI ====
st.markdown('<div class="subheader">💓 오늘의 감정은 어떤가요?</div>', unsafe_allow_html=True)

# 감정 데이터
emotions = {
    "행복": "😄", "기대": "🤩", "편안함": "😊",
    "무덤덤": "😐", "불안": "😟", "분노": "😡", "슬픔": "😞"
}

cols = st.columns(len(emotions))

for idx, (emo, emoji) in enumerate(emotions.items()):
    with cols[idx]:
        if st.button(f"{emoji}\n{emo}", key=f"emotion_{idx}"):
            st.session_state.mood = {"emotion": emo, "emoji": emoji}
            st.session_state.selected_index = idx

# 선택된 감정 표시
if st.session_state.mood:
    selected_emoji = st.session_state.mood["emoji"]
    selected_emotion = st.session_state.mood["emotion"]
    st.markdown(
        f"<div class='selected-mood-box'>선택한 감정: {selected_emoji} {selected_emotion}</div>",
        unsafe_allow_html=True
    )

# ==== 입력창 ====
st.markdown('<div class="subheader">✏️ 오늘의 감정 기록하기</div>', unsafe_allow_html=True)
mood_text = st.text_area("", key="mood_text", placeholder="오늘 월급 통장 스쳐 지나가서 살짝 슬픔...💸")

st.markdown('<div class="subheader">🗓️ 오늘의 일정 기록하기</div>', unsafe_allow_html=True)
schedule_text = st.text_area("", key="schedule_text", placeholder="11시 상사 잔소리 청취\n3시 두근두근 연봉협상\n5시 탈출 성공 기원하며 자리 정리")

# ==== 결과 생성 ====
if st.button("오늘 나의 기부니"):
    if not (st.session_state.mood and mood_text and schedule_text):
        st.warning("모든 입력을 완료해주세요!")
    else:
        loading_area = st.empty()  # 빈 영역 생성

        with loading_area.container():  # 로딩 표시
            st.markdown("""
            <div style='display: flex; align-items: center; justify-content: center; margin-top: 2rem;'>
                <div style="
                    border: 4px solid #f3f3f3;
                    border-top: 4px solid #E9428E;
                    border-radius: 50%;
                    width: 24px;
                    height: 24px;
                    animation: spin 1s linear infinite;
                    margin-right: 10px;
                "></div>
                <div style='color: #E9428E; font-style: italic; font-size: 16px;'>
                    💌 두근두근… 기부니가 당신의 하루를 분석하고 있어요!<br>잠시 기다려 주시면, 사랑 가득 담아 전해드릴게요 🌷🌷
                </div>
            </div>
            <style>
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            </style>
            """, unsafe_allow_html=True)
            
            # --- 날씨 호출 (생략 가능) ---
            try:
                sk = st.secrets["SERVICE_KEY"]
                END = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"
                today = datetime.today().strftime("%Y%m%d")
                now = datetime.now(); hr = now.hour
                if hr < 2:
                    bt, bd = "2300", (now - timedelta(days=1)).strftime("%Y%m%d")
                elif hr < 5:
                    bt, bd = "0200", today
                elif hr < 8:
                    bt, bd = "0500", today
                elif hr < 11:
                    bt, bd = "0800", today
                elif hr < 14:
                    bt, bd = "1100", today
                elif hr < 17:
                    bt, bd = "1400", today
                elif hr < 20:
                    bt, bd = "1700", today
                elif hr < 23:
                    bt, bd = "2000", today
                else:
                    bt, bd = "2300", today
                params = {
                    "serviceKey": sk, "numOfRows": "10", "pageNo": "1",
                    "dataType": "JSON", "base_date": bd, "base_time": bt,
                    "nx": "60", "ny": "127"
                }
                r = requests.get(END, params=params)
                if r.status_code == 200:
                    items = r.json()["response"]["body"]["items"]["item"]
                    tgt = {x["category"]: x["fcstValue"] for x in items if x["category"] in ["TMP","REH","POP","WSD"]}
                    weather = (
                        f"기온 {tgt.get('TMP','?')}°C, 습도 {tgt.get('REH','?')}%, "
                        f"강수확률 {tgt.get('POP','?')}%, 바람 {tgt.get('WSD','?')}m/s"
                    )
                else:
                    weather = "날씨 정보 없음"
            except:
                weather = "날씨 정보 없음"

            # --- GPT 프롬프트 + JSON 요청 ---

            prompt = f"""
당신은 감정+스케줄+날씨 전문가입니다. 모든 답변의 첫 부분에 다음 내용을 넣어주세요.

"어서오세요. 기분이 태도가 되는 세상입니다. 오늘 당신은 어떤 태도로 세상을 살아가실 건가요?"

[감정 입력]
{st.session_state.mood['emoji']} {st.session_state.mood['emotion']} ➔ "{mood_text}"

[스케줄 입력]
"{schedule_text}"

[🌷조언]

(감정, 스케줄, 날씨를 고려하여 솔루션 박사의 관점으로 조언)

[🧐오늘의 퇴사지수]

1~100%로 표현

[🍀솔루션 제안]
- 일정 조정
- 점심 추천
- 리프레시 방법

[🌈슬로건]

(오늘 당신의 태도를 요약하는 한 줄 문구)

[🙋🏻‍♀️엔딩]

"기분이 태도가 됐다. 조심해서 살아남으세요. 내일 또 봐요!"

날씨 정보: {weather}

위 텍스트를 그대로 출력해주세요.

추가로, **마지막에** 다음 JSON을 덧붙여 응답해주세요:
{{"result": string, "scores": {{"Energy": int, "Happiness": int, "Focus": int, "Calm": int}}}}
"""
            res = client.chat.completions.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])
            raw = res.choices[0].message.content

            # JSON 분리
            m = re.search(r'(\{.*\})\s*$', raw.strip(), re.DOTALL)
            if m:
                scores = json.loads(m.group(1))["scores"]
                text = raw[:m.start()].strip()
            else:
                text = raw
                scores = {"Energy": 0, "Happiness": 0, "Focus": 0, "Calm": 0}
        
        # ==== UI 표시 ====
        st.markdown(f"<div class='date'>{datetime.now():%Y년 %m월 %d일 (%A)}</div>", unsafe_allow_html=True)

        # 텍스트 전체 필터링: 감정/스케줄/날씨 구간 제외
        lines = text.splitlines()
        clean_lines = []
        skip_section = None
        for line in lines:
            if line.startswith("[감정 입력]"):
                skip_section = "emotion"
                continue
            if line.startswith("[스케줄 입력]"):
                skip_section = "schedule"
                continue
            if skip_section and re.match(r'^\[.*\]$', line) \
               and not line.startswith("[감정 입력]") \
               and not line.startswith("[스케줄 입력]"):
                skip_section = None
            if skip_section:
                continue
            if line.startswith("날씨 정보"):
                continue
            clean_lines.append(line)
        clean_text = "\n".join(clean_lines)
        
        loading_area.empty()  # 결과 오면 로딩창 지우기!

        st.markdown(f"<div class='glass-card'><pre style='font-family:inherit'>{clean_text}</pre></div>", unsafe_allow_html=True)

        # 네 가지 지표로 운세 표시
        st.markdown("<div class='subheader'>오늘의 감정 차트</div>", unsafe_allow_html=True)
        
        # 여백 추가
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # 지표 아이콘 정의
        indicators = {
            "Energy": "⚡",
            "Happiness": "😊",
            "Focus": "🎯",
            "Calm": "🧘"
        }
        
        # 지표별 한글 이름
        kr_names = {
            "Energy": "에너지",
            "Happiness": "행복도",
            "Focus": "집중도",
            "Calm": "평온함"
        }
        
        # 각 지표에 대한 프로그레스 바 표시
        for key, value in scores.items():
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                st.markdown(f"<div style='text-align: right; padding-top: 4px;'>{indicators[key]} {kr_names[key]}</div>", unsafe_allow_html=True)
            with col2:
                st.progress(value/100)
            with col3:
                st.markdown(f"<div style='padding-top: 4px; color: var(--pink-dark); font-weight: bold;'>{value}%</div>", unsafe_allow_html=True)
        
        st.balloons()

# ==== 하단 푸터 ====
st.markdown("""
<div style='margin-top:5rem;'>
    <hr style='border: none; border-top: 0.8px solid #ccc;'/>
    <p style='text-align:center; font-size: 13px; color: #aaa;'>
        © 2025 Gibooni Inc. All rights reserved. <br>
        기부니가 오늘도 당신의 하루를 응원합니다 💖
    </p>
</div>
""", unsafe_allow_html=True)
