# 영업권 평가 시스템 (Goodwill Valuation System)

이 프로젝트는 기업의 영업권 평가를 위한 Streamlit 기반 웹 애플리케이션입니다.

## 주요 기능

* 영업권 평가: 단계별 영업권 평가 및 예측/실적 비교 분석
* 다양한 평가 방법: 초과이익법, 시장가치법 지원
* 시각화: 그래프와 차트를 통한 직관적인 결과 제공

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
streamlit run main.py
```

## 개발 환경

- Python 3.7+
- Streamlit
- Pandas
- Numpy
- Plotly

## 라이선스

MIT License 