# 재무계산기 (Financial Calculator)

이 프로젝트는 다양한 재무 계산 도구를 제공하는 Streamlit 기반 웹 애플리케이션입니다.

## 주요 기능

- **예적금 계산기**: 단리/복리 비교 및 예금/적금 비교 기능 제공
- **복리 계산**: 연복리, 반기복리, 분기복리, 월복리, 일복리 계산
- **시각화**: 그래프와 차트를 통한 직관적인 비교 제공

## 설치 방법

1. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 실행 방법

```bash
streamlit run savings_calculator.py
```

## 기술 스택

- Python
- Streamlit
- Pandas
- NumPy
- Plotly 