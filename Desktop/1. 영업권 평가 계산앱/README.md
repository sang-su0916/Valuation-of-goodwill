# AI 기반 영업권 평가 시스템

Gemini AI를 활용한 지능형 영업권 평가 시스템입니다.

## 주요 기능

- AI 기반 평가 방법 추천
- 수익가치법, 시장가치법, 원가법 지원
- AI 기반 평가 결과 검증
- 자동 보고서 생성
- 시각화된 결과 제공

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/your-username/goodwill-valuation-ai.git
cd goodwill-valuation-ai
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 의존성 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
- `.env` 파일을 생성하고 Gemini API 키 설정
```
GEMINI_API_KEY=your_api_key_here
```

## 실행 방법

```bash
streamlit run app.py
```

## 사용 방법

1. 기업 정보 입력
   - 회사명
   - 산업 분류
   - 재무 정보

2. AI 추천 받기
   - 입력된 정보를 바탕으로 최적의 평가 방법 추천

3. 평가 수행
   - 선택한 방법으로 영업권 평가
   - AI 기반 결과 검증
   - 상세 보고서 생성

## 기술 스택

- Python
- Streamlit
- Google Gemini AI
- Plotly
- Pandas

## 라이선스

MIT License 