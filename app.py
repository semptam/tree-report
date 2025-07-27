import streamlit as st
import pandas as pd
import random
import requests
import re

# 데이터 불러오기
df = pd.read_csv("sample_tree_sensor_data.csv")
df = df.dropna()

st.title("오늘의 나무 리포트 🌳")

if st.button("리포트 생성하기"):
    # 랜덤 행 선택
    random_row = df.sample(n=1).iloc[0]
    random_date = random_row['timestamp']

    # 프롬프트 작성
    prompt = f"""
    너는 나무다. 아래의 데이터를 바탕으로 150자의 시적인 저널을 한국어로 작성해라.
    저널 맨 앞에 날짜({random_date})를 그대로 적고, 불필요한 머리말 없이 바로 글을 시작해라.
    인간이 나무의 감각을 체험할 수 있도록 생생하게 표현하되,
    환경 문제에 대한 경각심을 불러일으키는 어조로 작성해라.

    - Temperature: {random_row['temperature_C']} °C
    - Humidity: {random_row['humidity_%']} %
    - Soil moisture: {random_row['soil_moisture_%']} %
    - Light intensity: {random_row['light_lux']} lux
    """

    # OpenRouter API 요청
    api_key = st.secrets["OPENROUTER_API_KEY"]
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {
        "model": "meta-llama/llama-3-8b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    result_text = response.json()["choices"][0]["message"]["content"]

    # 불필요한 기호 제거
    cleaned_text = re.sub(r"^[^가-힣0-9]+", "", result_text).strip()

    # 출력
    st.markdown(f"### {random_date}")
    st.write(cleaned_text)
