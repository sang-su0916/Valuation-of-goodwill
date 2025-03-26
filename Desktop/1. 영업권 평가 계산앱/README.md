# 영업권 평가 시스템 (Goodwill Valuation System)

이 프로젝트는 다양한 재무 계산 도구를 제공하는 Streamlit 기반 웹 애플리케이션입니다.

## 주요 기능

* 영업권 계산: 단계별 영업권 평가 및 예측/실적 비교 기능 제공
* 복리 계산: 연복리, 반기복리, 분기복리, 월복리, 일복리 계산
* 시각화: 그래프와 차트를 통한 직관적인 비교 제공

## 설치 방법

1. 가상환경 생성 및 활성화

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

2. 필요한 패키지 설치

```
pip install -r requirements.txt
```

3. 애플리케이션 실행

```
streamlit run app.py
```

## 개발 환경

- Python 3.7+
- Streamlit
- Pandas
- Numpy
- Plotly

## 라이선스

MIT License 