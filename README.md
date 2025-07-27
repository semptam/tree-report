# 오늘의 나무 리포트 앱

이 앱은 나무 센서 데이터(CSV)를 기반으로 매일 랜덤하게 'Tree Correspondents 스타일' 저널을 생성합니다.  
OpenRouter API를 사용해 LLM 모델(Llama 3 등)과 연결하며, Streamlit Cloud에서 무료로 배포할 수 있습니다.

## 실행 방법

### 1. 로컬 실행

### 2. Streamlit Cloud 배포
1. 이 리포지토리를 GitHub에 업로드  
2. [Streamlit Cloud](https://streamlit.io/cloud)에서 앱 생성  
3. Settings → Secrets 메뉴에서 아래 추가:

4. 배포 후 발급된 URL로 접속

---

## 필요 패키지
- streamlit
- pandas
- requests
