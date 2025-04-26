import streamlit as st
from datetime import datetime
import time

# 페이지 설정
st.set_page_config(page_title="오늘의 마음 기록 결과", layout="centered")

# CSS 스타일 주입
st.markdown(
    '''
    <style>
    body {
        font-family: 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif;
        background-color: #fdf2f8;
        padding: 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(219, 39, 119, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.8);
    }
    h1 {
        font-size: 2.5rem;
        font-weight: 800;
        font-style: italic;
        color: #DB2777;
        transform: rotate(-1deg);
        margin-bottom: 0.25rem;
        text-align: center;
    }
    .date {
        color: gray;
        margin-top: -0.5rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    h3 { color: #DB2777; margin-top: 0; }
    .mood-label { font-size: 1.5rem; font-weight: bold; color: #DB2777; }
    .mood-comment { color: gray; }
    .progress-container {
        display: flex; justify-content: space-between; margin-bottom: 0.5rem;
    }
    .progress-bar {
        width: 100%; height: 8px; background-color: #f3f3f3;
        border-radius: 4px; margin-bottom: 1rem; position: relative;
    }
    .progress-fill {
        height: 100%; background-color: #DB2777;
        border-radius: 4px; position: absolute; top: 0; left: 0;
    }
    .timeline-entry { margin-bottom: 1rem; }
    .insights {
        background: rgba(255,255,255,0.7); backdrop-filter: blur(10px);
        border-radius: 16px; padding: 1rem; margin: 1.5rem 0;
        box-shadow: 0 4px 30px rgba(0,0,0,0.1);
    }
    .insights-header { display: flex; align-items: center; margin-bottom: 0.75rem; }
    .insights-icon { font-size: 1.25rem; color: #DB2777; margin-right: 0.5rem; }
    .insights-title { margin: 0; font-weight: 600; color: #DB2777; }
    .insights-list { list-style: none; padding: 0; margin: 0; }
    .insight-item { display: flex; align-items: flex-start; margin-bottom: 0.5rem; }
    .insight-marker {
        display: inline-block; width: 1rem; color: #FF75BB;
        font-weight: bold; margin-right: 0.5rem;
    }
    .insight-text { margin: 0; color: #4F4F4F; font-size: 0.9rem; }
    </style>
    ''',
    unsafe_allow_html=True
)

# 풍선 효과 (Streamlit 네이티브)
st.balloons()
time.sleep(0.5)

# 헤더
now = datetime.now()
st.markdown(f"<h1>오늘의 마음 기록</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='date'>{now.strftime('%Y년 %m월 %d일 (%A)')}</p>", unsafe_allow_html=True)

# 샘플 데이터
moodData = {
    'overall': '행복해요 😄',
    'comment': '프로젝트 마감했다! 오늘은 정말 생산적인 하루였어',
    'moodScore': {
        'Energy': 85,
        'Happiness': 90,
        'Focus': 75,
        'Calm': 60
    },
    'timeline': [
        {'time': '09:00', 'label': '상쾌함 😊', 'note': '아침 운동 후 개운해요'},
        {'time': '11:30', 'label': '팀 미팅', 'note': '프로젝트 진행상황 논의'},
        {'time': '14:00', 'label': '집중 중 🧠', 'note': '코드 리뷰 작업 중'},
        {'time': '17:00', 'label': '뿌듯함 😄', 'note': '프로젝트 마감 성공!'}
    ],
    'insights': [
        "친구와의 만남이 당신의 기분을 크게 향상시켰습니다.",
        "업무 관련 일정 전에 불안감이 증가하는 패턴이 있습니다.",
        "신체 활동이 기분 전환에 큰 도움이 되는 것 같습니다."
    ]
}

# 오늘의 기분 카드
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<h3>오늘의 기분</h3>", unsafe_allow_html=True)
st.markdown(f"<div class='mood-label'>{moodData['overall']}</div>", unsafe_allow_html=True)
st.markdown(f"<p class='mood-comment'>{moodData['comment']}</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 인사이트 카드
st.markdown("<div class='insights'>", unsafe_allow_html=True)
st.markdown("<div class='insights-header'><span class='insights-icon'>🏆</span><h3 class='insights-title'>인사이트</h3></div>", unsafe_allow_html=True)
st.markdown("<ul class='insights-list'>", unsafe_allow_html=True)
for insight in moodData['insights']:
    st.markdown(
        f"<li class='insight-item'><span class='insight-marker'>&gt;</span>"
        f"<p class='insight-text'>{insight}</p></li>",
        unsafe_allow_html=True
    )
st.markdown("</ul></div>", unsafe_allow_html=True)

# 감정 점수 카드
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<h3>감정 점수</h3>", unsafe_allow_html=True)
for label, score in moodData['moodScore'].items():
    st.markdown(
        f"<div class='progress-container'><span>{label}</span><span>{score}%</span></div>"
        "<div class='progress-bar'><div class='progress-fill' style='width:" + str(score) + "%'></div></div>",
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)

# 타임라인 카드
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<h3>하루 타임라인</h3>", unsafe_allow_html=True)
for entry in moodData['timeline']:
    st.markdown(
        f"<div class='timeline-entry'><strong>{entry['time']}</strong> &nbsp;"
        f"<span style='font-weight:600;'>{entry['label']}</span><br>"
        f"<small style='color:gray;'>{entry['note']}</small></div>",
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)
