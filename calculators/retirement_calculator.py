import streamlit as st
import pandas as pd
import numpy as np

def retirement_calculator():
    st.header("은퇴계산기")
    
    # 사용 방법 안내
    with st.expander("💡 은퇴계산기 사용 방법"):
        st.write("""
        은퇴 계산기를 사용하여 은퇴 준비 상태를 확인하세요:
        
        1. 현재 나이와 은퇴 희망 나이를 입력하세요.
        2. 현재 저축액과 연소득 정보를 입력하세요.
        3. 은퇴 후 필요한 월 생활비를 예상해 입력하세요.
        4. '계산하기' 버튼을 눌러 은퇴 준비 상태를 확인하세요.
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_age = st.number_input("현재 나이", min_value=20, max_value=70, value=30)
        retirement_age = st.number_input("은퇴 희망 나이", min_value=current_age + 1, max_value=90, value=65)
        life_expectancy = st.number_input("기대수명", min_value=retirement_age + 1, max_value=110, value=85)
        
        current_savings_text = st.text_input(
            "현재 저축액 (원)",
            value="50,000,000",
            help="숫자만 입력하세요. 예: 50000000"
        )
        try:
            current_savings = int(current_savings_text.replace(',', ''))
        except:
            current_savings = 50000000
    
    with col2:
        annual_income_text = st.text_input(
            "현재 연소득 (원)",
            value="50,000,000",
            help="숫자만 입력하세요. 예: 50000000"
        )
        try:
            annual_income = int(annual_income_text.replace(',', ''))
        except:
            annual_income = 50000000
        
        monthly_expenses_text = st.text_input(
            "은퇴 후 월 생활비 (원)",
            value="3,000,000",
            help="숫자만 입력하세요. 예: 3000000"
        )
        try:
            monthly_expenses = int(monthly_expenses_text.replace(',', ''))
        except:
            monthly_expenses = 3000000
        
        annual_return_rate = st.number_input(
            "투자 수익률 (%)",
            min_value=0.0,
            max_value=15.0,
            value=5.0,
            step=0.5
        )
        
        savings_rate = st.number_input(
            "연소득 중 저축 비율 (%)",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=5.0
        )
    
    if st.button("계산하기", key="retirement_button", use_container_width=True):
        # 계산 로직
        years_to_retirement = retirement_age - current_age
        retirement_duration = life_expectancy - retirement_age
        
        # 연간 저축액
        annual_savings = annual_income * (savings_rate / 100)
        monthly_savings = annual_savings / 12
        
        # 은퇴 자금 계산
        future_value = calculate_future_value(
            current_savings,
            monthly_savings,
            annual_return_rate / 100 / 12,
            years_to_retirement * 12
        )
        
        # 필요 은퇴 자금
        required_fund = calculate_required_retirement_fund(
            monthly_expenses,
            annual_return_rate / 100 / 12,
            retirement_duration * 12
        )
        
        # 결과 표시
        st.subheader("은퇴 준비 분석")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("예상 은퇴 자금", f"₩{future_value:,.0f}")
        col2.metric("필요 은퇴 자금", f"₩{required_fund:,.0f}")
        
        # 상태 표시
        if future_value >= required_fund:
            surplus = future_value - required_fund
            surplus_percentage = (surplus / required_fund) * 100
            col3.metric("상태", "충분", f"+₩{surplus:,.0f} ({surplus_percentage:.1f}%)")
            
            st.success(f"축하합니다! 현재 계획대로라면 은퇴 자금이 {surplus_percentage:.1f}% 정도 더 여유있게 준비될 것으로 예상됩니다.")
        else:
            deficit = required_fund - future_value
            deficit_percentage = (deficit / required_fund) * 100
            col3.metric("상태", "부족", f"-₩{deficit:,.0f} ({deficit_percentage:.1f}%)")
            
            st.warning(f"은퇴 자금이 {deficit_percentage:.1f}% 부족할 것으로 예상됩니다. 저축을 더 늘릴 필요가 있습니다.")
            
            # 개선 방안
            st.subheader("개선 방안")
            
            # 1. 저축률 늘리기
            additional_savings_needed = calculate_additional_savings_needed(
                deficit,
                annual_return_rate / 100 / 12,
                years_to_retirement * 12
            )
            
            st.info(f"매월 약 ₩{additional_savings_needed:,.0f}원을 추가로 저축하면 필요한 은퇴 자금을 마련할 수 있습니다.")
            
            # 2. 은퇴 나이 늘리기
            if retirement_age < 70:
                additional_years = 5
                new_retirement_age = retirement_age + additional_years
                new_years_to_retirement = new_retirement_age - current_age
                new_retirement_duration = life_expectancy - new_retirement_age
                
                new_future_value = calculate_future_value(
                    current_savings,
                    monthly_savings,
                    annual_return_rate / 100 / 12,
                    new_years_to_retirement * 12
                )
                
                new_required_fund = calculate_required_retirement_fund(
                    monthly_expenses,
                    annual_return_rate / 100 / 12,
                    new_retirement_duration * 12
                )
                
                if new_future_value >= new_required_fund:
                    st.info(f"은퇴 나이를 {additional_years}년 늘려 {new_retirement_age}세에 은퇴하면 자금이 충분할 것으로 예상됩니다.")
                else:
                    new_deficit = new_required_fund - new_future_value
                    new_deficit_percentage = (new_deficit / new_required_fund) * 100
                    st.info(f"은퇴 나이를 {additional_years}년 늘려도 여전히 {new_deficit_percentage:.1f}% 부족할 것으로 예상됩니다.")
        
        # 월별 저축 금액과 은퇴 후 인출 금액 표시
        st.subheader("월별 금액")
        col1, col2 = st.columns(2)
        col1.metric("현재 월 저축액", f"₩{monthly_savings:,.0f}")
        col2.metric("은퇴 후 월 생활비", f"₩{monthly_expenses:,.0f}")

def calculate_future_value(initial_investment, monthly_contribution, monthly_rate, total_months):
    """은퇴 시점의 자금을 계산합니다."""
    # 현재 저축의 성장
    future_savings = initial_investment * (1 + monthly_rate) ** total_months
    
    # 월 저축의 성장 (복리 적용)
    if monthly_rate > 0:
        future_contributions = monthly_contribution * ((1 + monthly_rate) ** total_months - 1) / monthly_rate
    else:
        future_contributions = monthly_contribution * total_months
    
    return future_savings + future_contributions

def calculate_required_retirement_fund(monthly_expenses, monthly_rate, retirement_months):
    """은퇴 생활에 필요한 자금을 계산합니다."""
    if monthly_rate > 0:
        # 현재 가치 계수(Present Value Annuity Factor)를 사용
        pv_factor = (1 - 1 / (1 + monthly_rate) ** retirement_months) / monthly_rate
        required_fund = monthly_expenses * pv_factor
    else:
        # 수익률이 0인 경우, 단순히 월 지출 * 개월 수
        required_fund = monthly_expenses * retirement_months
    
    return required_fund

def calculate_additional_savings_needed(deficit, monthly_rate, months):
    """부족한 자금을 마련하기 위한 추가 월 저축액을 계산합니다."""
    if monthly_rate > 0 and months > 0:
        # 미래 가치를 위한 월 납입액 공식의 역산
        additional_monthly = deficit * monthly_rate / ((1 + monthly_rate) ** months - 1)
    else:
        # 수익률이 0이거나 기간이 0인 경우
        additional_monthly = deficit / months if months > 0 else deficit
    
    return additional_monthly
