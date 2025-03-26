import streamlit as st
import pandas as pd
import numpy as np

def retirement_calculator():
    st.header("은퇴계산기")
    
    # 사용 방법 안내
    with st.expander("💡 은퇴계산기 사용 방법"):
        st.write("""
        쉽게 은퇴 준비 상태를 확인하세요:
        
        1. 기본 정보: 현재 나이, 은퇴 희망 나이, 기대수명을 입력하세요.
        2. 재정 상태: 현재 저축액, 월 소득과 지출을 입력하세요.
        3. 은퇴 후 희망 생활비를 입력하세요.
        4. '계산하기' 버튼을 눌러 은퇴 준비 상태와 필요한 저축 계획을 확인하세요.
        """)
    
    # 탭 구성
    tab1, tab2 = st.tabs(["기본 정보 입력", "상세 설정"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("개인 정보")
            current_age = st.number_input("현재 나이", min_value=20, max_value=70, value=30)
            retirement_age = st.number_input("은퇴 희망 나이", min_value=current_age + 1, max_value=90, value=65)
            life_expectancy = st.number_input("기대수명", min_value=retirement_age + 1, max_value=110, value=85)
            
            st.subheader("현재 재정 상태")
            current_savings_text = st.text_input(
                "현재 저축액 (원)",
                value="50,000,000",
                help="현재 은퇴를 위해 보유한 자산 총액"
            )
            try:
                current_savings = int(current_savings_text.replace(',', ''))
            except:
                current_savings = 50000000
        
        with col2:
            st.subheader("월 수입 및 지출")
            monthly_income_text = st.text_input(
                "월 소득 (원)",
                value="4,000,000",
                help="세후 월 소득"
            )
            try:
                monthly_income = int(monthly_income_text.replace(',', ''))
            except:
                monthly_income = 4000000
                
            monthly_current_expenses_text = st.text_input(
                "현재 월 생활비 (원)",
                value="3,000,000",
                help="현재 생활에 필요한 월 지출액"
            )
            try:
                monthly_current_expenses = int(monthly_current_expenses_text.replace(',', ''))
            except:
                monthly_current_expenses = 3000000
            
            st.subheader("은퇴 후 예상")
            retirement_expenses_text = st.text_input(
                "은퇴 후 월 생활비 (원)",
                value="2,500,000",
                help="은퇴 후 필요한 월 생활비 (현재 기준)"
            )
            try:
                retirement_expenses = int(retirement_expenses_text.replace(',', ''))
            except:
                retirement_expenses = 2500000
    
    with tab2:
        st.subheader("투자 및 저축 설정")
        col1, col2 = st.columns(2)
        
        with col1:
            annual_return_rate = st.slider(
                "예상 투자 수익률 (%)",
                min_value=0.0,
                max_value=15.0,
                value=5.0,
                step=0.5,
                help="은퇴 전후 평균 연간 투자 수익률"
            )
            
            inflation_rate = st.slider(
                "예상 물가상승률 (%)",
                min_value=0.0,
                max_value=10.0,
                value=2.0,
                step=0.1,
                help="연간 물가상승률"
            )
        
        with col2:
            monthly_savings = monthly_income - monthly_current_expenses
            max_possible_savings = max(monthly_income * 0.9, monthly_savings)
            
            target_monthly_savings_text = st.text_input(
                "월 저축 목표액 (원)",
                value=f"{monthly_savings:,.0f}",
                help="매월 은퇴를 위해 저축할 금액"
            )
            try:
                target_monthly_savings = int(target_monthly_savings_text.replace(',', ''))
            except:
                target_monthly_savings = monthly_savings
            
            retirement_withdraw_rate = st.slider(
                "연간 인출률 (%)",
                min_value=1.0,
                max_value=10.0,
                value=4.0,
                step=0.1,
                help="은퇴 후 자산에서 연간 인출할 비율 (일반적으로 4% 규칙 적용)"
            )
    
    if st.button("계산하기", key="retirement_button", use_container_width=True):
        # 기본 계산 로직
        years_to_retirement = retirement_age - current_age
        retirement_duration = life_expectancy - retirement_age
        
        # 인플레이션 적용한 은퇴 후 필요 생활비
        inflation_adjusted_expenses = retirement_expenses * ((1 + inflation_rate/100) ** years_to_retirement)
        
        # 월 저축액 (연간)
        annual_savings = target_monthly_savings * 12
        
        # 은퇴 시점에 예상되는 자산
        future_value = calculate_future_value(
            current_savings,
            target_monthly_savings,
            annual_return_rate / 100 / 12,
            years_to_retirement * 12
        )
        
        # 은퇴 후 필요 자금 계산 (인출률 기준)
        # 1) 4% 인출 규칙 기준 필요 자금
        required_fund_by_withdrawal = inflation_adjusted_expenses * 12 / (retirement_withdraw_rate / 100)
        
        # 2) 기대 수명 동안 필요한 자금 (수익률 고려)
        required_fund_by_duration = calculate_required_retirement_fund(
            inflation_adjusted_expenses,
            (annual_return_rate - inflation_rate) / 100 / 12,  # 실질 수익률 (인플레이션 감안)
            retirement_duration * 12
        )
        
        # 더 높은 금액을 필요 자금으로 설정 (안전 마진)
        required_fund = max(required_fund_by_withdrawal, required_fund_by_duration)
        
        # 결과 표시: 은퇴 자금 목표 및 현재 계획
        st.markdown("---")
        st.subheader("📊 은퇴 준비 요약")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("예상 은퇴 자금", f"₩{future_value:,.0f}")
        col2.metric("필요 은퇴 자금", f"₩{required_fund:,.0f}")
        
        funding_ratio = (future_value / required_fund) * 100
        
        # 상태 표시
        if future_value >= required_fund:
            surplus = future_value - required_fund
            col3.metric("달성률", f"{funding_ratio:.1f}%", f"+₩{surplus:,.0f}", delta_color="normal")
            
            st.success(f"👍 축하합니다! 현재 계획대로라면 은퇴 자금을 충분히 마련할 수 있습니다.")
            st.info(f"은퇴 시 약 ₩{surplus:,.0f}원(약 {(surplus/required_fund*100):.1f}%)의 여유 자금이 있을 것으로 예상됩니다.")
        else:
            deficit = required_fund - future_value
            col3.metric("달성률", f"{funding_ratio:.1f}%", f"-₩{deficit:,.0f}", delta_color="inverse")
            
            st.warning(f"⚠️ 현재 계획으로는 은퇴 자금이 부족할 것으로 예상됩니다.")
            
            # 개선 방안 표시
            st.markdown("---")
            st.subheader("💡 은퇴 준비 개선 방안")
            
            # 1. 저축 증액 방안
            additional_savings_needed = calculate_additional_savings_needed(
                deficit,
                annual_return_rate / 100 / 12,
                years_to_retirement * 12
            )
            
            current_vs_needed = st.columns(2)
            with current_vs_needed[0]:
                st.metric("현재 월 저축액", f"₩{target_monthly_savings:,.0f}")
            with current_vs_needed[1]:
                st.metric("필요 월 저축액", f"₩{target_monthly_savings + additional_savings_needed:,.0f}", 
                         f"+₩{additional_savings_needed:,.0f}", delta_color="inverse")
            
            st.info(f"💰 매월 약 ₩{additional_savings_needed:,.0f}원을 추가로 저축하면 목표 은퇴 자금을 달성할 수 있습니다.")
            
            # 2. 은퇴 연령 조정 방안
            if retirement_age < 70:
                adjusted_retirement_ages = []
                for additional_years in [3, 5, 7]:
                    new_retirement_age = retirement_age + additional_years
                    new_years_to_retirement = new_retirement_age - current_age
                    new_retirement_duration = life_expectancy - new_retirement_age
                    
                    # 추가 기간 동안의 자산 성장
                    new_future_value = calculate_future_value(
                        current_savings,
                        target_monthly_savings,
                        annual_return_rate / 100 / 12,
                        new_years_to_retirement * 12
                    )
                    
                    # 줄어든 은퇴 기간에 따른 필요 자금 재계산
                    new_inflation_adjusted_expenses = retirement_expenses * ((1 + inflation_rate/100) ** new_years_to_retirement)
                    
                    new_required_fund_by_duration = calculate_required_retirement_fund(
                        new_inflation_adjusted_expenses,
                        (annual_return_rate - inflation_rate) / 100 / 12,
                        new_retirement_duration * 12
                    )
                    
                    new_required_fund_by_withdrawal = new_inflation_adjusted_expenses * 12 / (retirement_withdraw_rate / 100)
                    new_required_fund = max(new_required_fund_by_withdrawal, new_required_fund_by_duration)
                    
                    funding_ratio = (new_future_value / new_required_fund) * 100
                    adjusted_retirement_ages.append({
                        "years": additional_years,
                        "age": new_retirement_age,
                        "funded_ratio": funding_ratio,
                        "sufficient": new_future_value >= new_required_fund
                    })
                
                st.write("⏰ 은퇴 시기 조정 효과:")
                
                age_cols = st.columns(len(adjusted_retirement_ages))
                for i, age_option in enumerate(adjusted_retirement_ages):
                    with age_cols[i]:
                        st.metric(f"{age_option['age']}세에 은퇴", 
                                 f"{age_option['funded_ratio']:.1f}% 달성", 
                                 f"+{age_option['years']}년 지연",
                                 delta_color="off")
                        if age_option['sufficient']:
                            st.success("목표 달성 가능")
                        else:
                            st.warning("추가 저축 필요")
            
            # 3. 수익률 조정 방안
            if annual_return_rate < 12.0:
                st.write("📈 투자 수익률 조정 효과:")
                
                return_cols = st.columns(3)
                for i, additional_return in enumerate([1.0, 2.0, 3.0]):
                    new_return_rate = annual_return_rate + additional_return
                    
                    # 높은 수익률로 자산 재계산
                    new_future_value = calculate_future_value(
                        current_savings,
                        target_monthly_savings,
                        new_return_rate / 100 / 12,
                        years_to_retirement * 12
                    )
                    
                    funding_ratio = (new_future_value / required_fund) * 100
                    
                    with return_cols[i]:
                        st.metric(f"수익률 {new_return_rate:.1f}%", 
                                 f"{funding_ratio:.1f}% 달성", 
                                 f"+{additional_return:.1f}%p",
                                 delta_color="off")
                        if new_future_value >= required_fund:
                            st.success("목표 달성 가능")
                        else:
                            st.warning("추가 조정 필요")
        
        # 은퇴 자금 세부 정보
        st.markdown("---")
        st.subheader("🔎 은퇴 자금 세부 정보")
        
        detail_cols = st.columns(2)
        
        with detail_cols[0]:
            st.write("**은퇴 전 자산 축적 계획**")
            st.metric("은퇴까지 남은 기간", f"{years_to_retirement}년")
            st.metric("현재 저축액", f"₩{current_savings:,.0f}")
            st.metric("월 저축액", f"₩{target_monthly_savings:,.0f}")
            st.metric("연간 투자 수익률", f"{annual_return_rate:.1f}%")
            st.metric("은퇴 시점 예상 자산", f"₩{future_value:,.0f}")
        
        with detail_cols[1]:
            st.write("**은퇴 후 필요 자금**")
            st.metric("은퇴 후 예상 기간", f"{retirement_duration}년")
            st.metric("현재 기준 월 생활비", f"₩{retirement_expenses:,.0f}")
            st.metric("은퇴 시점 월 생활비", f"₩{inflation_adjusted_expenses:,.0f}")
            st.metric("연간 인출률", f"{retirement_withdraw_rate:.1f}%")
            st.metric("필요 은퇴 자금", f"₩{required_fund:,.0f}")

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
