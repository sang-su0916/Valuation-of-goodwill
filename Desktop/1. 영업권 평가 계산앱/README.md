# 영업권 평가 시스템 (Goodwill Valuation System)

이 프로젝트는 기업의 영업권 가치를 평가하기 위한 Streamlit 기반 웹 애플리케이션입니다.

## 주요 기능

* **영업권 가치평가**: 기업의 재무 데이터를 기반으로 영업권 가치를 계산합니다.
* **다양한 평가 방법론**: 초과이익법, 현금흐름할인법(DCF) 등 다양한 방법론을 지원합니다.
* **직관적인 UI**: 사용자 친화적인 인터페이스로 간편하게 평가할 수 있습니다.
* **결과 시각화**: 그래프와 차트를 통해 평가 결과를 시각적으로 표현합니다.

## 설치 방법

1. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

3. 애플리케이션 실행

```bash
streamlit run main.py
```

## 사용 방법

1. 회사명, 평가 기준일 등 기본 정보를 입력합니다.
2. 매출액, 영업이익 등 재무 정보를 입력합니다.
3. 성장률, 할인율 등 평가에 필요한 매개변수를 설정합니다.
4. '평가 계산' 버튼을 클릭하여 결과를 확인합니다.

## 기술 스택

- Python 3.7+
- Streamlit
- Pandas (추후 추가 예정)
- Plotly (추후 추가 예정)

## 라이선스

MIT License 