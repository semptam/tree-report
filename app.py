import streamlit as st
import pandas as pd
import random
import requests
import re

# ===========================================
# 1. 데이터 불러오기
# ===========================================
df = pd.read_csv("sample_tree_sensor_data.csv")
df = df.dropna()

# ===========================================
# 2. 앱 UI
# ===========================================
st.title("오늘의 나무 리포트 🌳")

if st.button("리포트 생성하기"):
    # 랜덤 데이터 선택
    random_row = df.sample(n=1).iloc[0]
    random_date = random_row['timestamp']

    # ===========================================
    # 3. 프롬프트 (한국어 강화)
    # ===========================================
    prompt = f"""
    너는 나무다. 아래 데이터를 활용해 150자 이내의 시적인 저널을 **한국어로만** 작성하라.
    영어, 외래어, 특수문자를 사용하지 말고 자연스러운 한국어 문장으로 표현해라.
    저널은 날짜({random_date})로 시작하고, 나무의 감각과 환경에 대한 경각심을 생생히 전해라.

    - 온도: {random_row['temperature_C']} °C
    - 습도: {random_row['humidity_%']} %
    - 토양 수분: {random_row['soil_moisture_%']} %
    - 빛 세기: {random_row['light_lux']} lux
    """

    # ===========================================
    # 4. OpenRouter API 호출
    # ===========================================
    api_key = st.secrets["OPENROUTER_API_KEY"]
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": "meta-llama/llama-3-8b-instruct"",  # 한국어 품질 좋은 모델
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    # ===========================================
    # 5. 결과 후처리 (영어/특수문자 제거)
    # ===========================================
    result_text = response.json()["choices"][0]["message"]["content"]

    # 불필요한 영어/특수문자 제거 후 한국어만 남김
    cleaned_text = re.sub(r'[^가-힣0-9\s\.\,\-\%\(\)]', '', result_text).strip()

    # ===========================================
    # 6. 출력
    # ===========================================
    st.markdown(f"### {random_date}")
    st.write(cleaned_text)

result = response.json()

if "choices" in result:
    result_text = result["choices"][0]["message"]["content"]
else:
    st.error(f"API 호출 실패: {result}")
    st.stop()

