# 영업권 평가 시스템 - Phase 1 구현

# 이 파일은 이전 버전의 구현입니다.
# 현재는 main.py로 새롭게 구현되었습니다.

# 자세한 내용은 main.py를 참고하세요.
# 혹은 터미널에서 아래 명령어로 새 애플리케이션을 실행하세요:
# streamlit run main.py

import streamlit as st
import pandas as pd
import numpy as np

# 페이지 기본 설정
st.set_page_config(
    page_title="영업권 평가 시스템",
    page_icon="💼",
    layout="wide"
)

# 메인 타이틀
st.title("영업권 평가 시스템")
st.write("기업의 영업권 가치를 평가하기 위한 도구입니다.")

# 사이드바 설정
with st.sidebar:
    st.header("평가 방법 선택")
    valuation_method = st.selectbox(
        "평가 방법",
        ["초과이익법", "현금흐름할인법(DCF)", "시장가치비교법"]
    )

# 기본 정보 입력
st.header("기업 정보 입력")
col1, col2 = st.columns(2)

with col1:
    company_name = st.text_input("회사명", "")
    industry = st.selectbox("산업군", ["제조업", "서비스업", "IT/소프트웨어", "유통/물류", "금융", "기타"])
    
with col2:
    def format_number(value):
        """숫자를 콤마가 포함된 문자열로 변환"""
        try:
            return f"{int(float(value)):,}"
        except (ValueError, TypeError):
            return ""

    def parse_number(value):
        """콤마가 포함된 문자열을 숫자로 변환"""
        try:
            return float(value.replace(",", ""))
        except (ValueError, TypeError):
            return 0.0

    # 사업 운영 기간 입력
    business_years_input = st.text_input("사업 운영 기간(년)", value=format_number(business_years))
    if business_years_input:
        business_years = int(parse_number(business_years_input))

    # 직원 수 입력
    employee_count_input = st.text_input("직원 수", value=format_number(employee_count))
    if employee_count_input:
        employee_count = int(parse_number(employee_count_input))

# 재무 정보 입력
st.header("재무 정보")
col3, col4 = st.columns(2)

with col3:
    # 매출액 입력
    revenue_input = st.text_input("매출액 (백만원)", value=format_number(revenue))
    if revenue_input:
        revenue = parse_number(revenue_input)

    # 영업이익 입력
    operating_profit_input = st.text_input("영업이익 (백만원)", value=format_number(operating_profit))
    if operating_profit_input:
        operating_profit = parse_number(operating_profit_input)
    
with col4:
    # 당기순이익 입력
    net_income_input = st.text_input("당기순이익 (백만원)", value=format_number(net_income))
    if net_income_input:
        net_income = parse_number(net_income_input)

    # 총자산 입력
    total_assets_input = st.text_input("총자산 (백만원)", value=format_number(total_assets))
    if total_assets_input:
        total_assets = parse_number(total_assets_input)

# 성장률 및 할인율 입력
st.header("평가 매개변수")
col5, col6 = st.columns(2)

with col5:
    growth_rate = st.slider("성장률 (%)", min_value=0.1, max_value=30.0, value=5.0)
    discount_rate = st.slider("할인율 (%)", min_value=0.1, max_value=30.0, value=10.0)
    
with col6:
    forecast_years = st.slider("예측 기간 (년)", min_value=1, max_value=10, value=5)
    risk_premium = st.slider("위험 프리미엄 (%)", min_value=0.0, max_value=10.0, value=3.0)

# 계산 버튼
if st.button("평가 계산", type="primary"):
    # 선택된 방법에 따른 계산 로직
    if valuation_method == "초과이익법":
        # 초과이익법 계산
        normal_profit_rate = 0.05  # 정상이익률 (예시)
        normal_profit = total_assets * normal_profit_rate
        excess_profit = operating_profit - normal_profit
        goodwill_value = excess_profit * 5  # 5년치 초과이익
        
        # 결과 표시
        st.success(f"영업권 평가액: {goodwill_value:,.1f} 백만원")
        
        # 계산 과정 표시
        st.subheader("계산 과정")
        st.write(f"1. 정상이익 = 총자산({total_assets:,.1f}백만원) × 정상이익률({normal_profit_rate*100:.1f}%) = {normal_profit:,.1f}백만원")
        st.write(f"2. 초과이익 = 영업이익({operating_profit:,.1f}백만원) - 정상이익({normal_profit:,.1f}백만원) = {excess_profit:,.1f}백만원")
        st.write(f"3. 영업권 = 초과이익({excess_profit:,.1f}백만원) × 5년 = {goodwill_value:,.1f}백만원")
        
    elif valuation_method == "현금흐름할인법(DCF)":
        # DCF 방법 계산
        cash_flows = []
        for year in range(1, forecast_years + 1):
            cf = operating_profit * (1 + growth_rate/100) ** year
            cash_flows.append(cf)
        
        # 현재가치 계산
        present_values = []
        for i, cf in enumerate(cash_flows):
            pv = cf / ((1 + discount_rate/100) ** (i+1))
            present_values.append(pv)
        
        goodwill_value = sum(present_values)
        
        # 결과 표시
        st.success(f"영업권 평가액: {goodwill_value:,.1f} 백만원")
        
        # 계산 과정 테이블 표시
        df = pd.DataFrame({
            '연도': [f'{i+1}년차' for i in range(forecast_years)],
            '예상 현금흐름': cash_flows,
            '할인율': [f'{discount_rate}%' for _ in range(forecast_years)],
            '현재가치': present_values
        })
        
        st.subheader("DCF 계산 과정")
        st.dataframe(df)
        
    else:  # 시장가치비교법
        # 시장가치비교법 계산 (단순 예시)
        industry_multiple = 8  # 업종 평균 배수 (예시)
        goodwill_value = operating_profit * industry_multiple
        
        # 결과 표시
        st.success(f"영업권 평가액: {goodwill_value:,.1f} 백만원")
        
        # 계산 과정 표시
        st.subheader("계산 과정")
        st.write(f"영업권 = 영업이익({operating_profit:,.1f}백만원) × 업종 평균 배수({industry_multiple}) = {goodwill_value:,.1f}백만원")
        
    # 추가 정보
    st.info("상세 결과 분석 기능은 개발 중입니다. 현재는 기본적인 계산 결과만 제공됩니다.") 