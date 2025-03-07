import streamlit as st
import pandas as pd
import numpy as np

def investment_calculator():
    st.header("투자계산기")
    
    # 사용 방법 안내
    with st.expander("💡 투자계산기 사용 방법"):
        st.write("""
        이 투자계산기로 미래 가치(FV)와 현재 가치(PV) 계산을 할 수 있습니다.
        
        **미래가치(FV) 계산**: 현재 투자금액이 미래에 얼마가 될지 계산합니다.
        **현재가치(PV) 계산**: 미래에 필요한 금액을 위해 현재 얼마를 투자해야 할지 계산합니다.
        """)
    
    # 계산 유형 선택
    calc_type = st.radio(
        "계산 유형",
        options=["미래가치(FV) 계산", "현재가치(PV) 계산"],
        horizontal=True
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if calc_type == "미래가치(FV) 계산":
            initial_investment_text = st.text_input(
                "초기투자금액 (원)",
                value="10,000,000",
                help="숫자만 입력하세요. 예: 10000000"
            )
            try:
                initial_investment = int(initial_investment_text.replace(',', ''))
            except:
                initial_investment = 10000000
        else:
            target_amount_text = st.text_input(
                "목표금액 (원)",
                value="100,000,000",
                help="숫자만 입력하세요. 예: 100000000"
            )
            try:
                target_amount = int(target_amount_text.replace(',', ''))
            except:
                target_amount = 100000000
            
        monthly_contribution_text = st.text_input(
            "월 투자금액 (원)",
            value="500,000",
            help="숫자만 입력하세요. 예: 500000"
        )
        try:
            monthly_contribution = int(monthly_contribution_text.replace(',', ''))
        except:
            monthly_contribution = 500000
    
    with col2:
        investment_period = st.number_input(
            "투자기간 (년)",
            min_value=1,
            max_value=50,
            value=10
        )
        
        annual_return = st.number_input(
            "연수익률 (%)",
            min_value=0.0,
            max_value=30.0,
            value=7.0,
            step=0.5
        )
    
    if st.button("계산하기", key="investment_button", use_container_width=True):
        monthly_rate = annual_return / 12 / 100
        total_months = investment_period * 12
        
        if calc_type == "미래가치(FV) 계산":
            # 미래가치 계산
            future_value = calculate_future_value(initial_investment, monthly_contribution, monthly_rate, total_months)
            total_invested = initial_investment + monthly_contribution * total_months
            investment_gain = future_value - total_invested
            
            # 결과 표시
            st.subheader("투자 결과")
            col1, col2, col3 = st.columns(3)
            col1.metric("미래 가치", f"₩{future_value:,.0f}")
            col2.metric("총 투자금액", f"₩{total_invested:,.0f}")
            col3.metric("투자 수익", f"₩{investment_gain:,.0f}", f"{investment_gain/total_invested*100:.1f}%")
            
        else:
            # 현재가치 계산
            present_value = calculate_present_value(target_amount, monthly_contribution, monthly_rate, total_months)
            total_contribution = monthly_contribution * total_months
            total_required = present_value + total_contribution
            future_gain = target_amount - total_required
            
            # 결과 표시
            st.subheader("투자 결과")
            col1, col2, col3 = st.columns(3)
            col1.metric("필요 초기 투자금", f"₩{present_value:,.0f}")
            col2.metric("총 월 납입금", f"₩{total_contribution:,.0f}")
            col3.metric("투자 수익", f"₩{future_gain:,.0f}", f"{future_gain/total_required*100:.1f}%")
        
        # 투자 그래프 표시
        if calc_type == "미래가치(FV) 계산":
            df = generate_investment_data(initial_investment, monthly_contribution, monthly_rate, total_months)
        else:
            df = generate_investment_data(present_value, monthly_contribution, monthly_rate, total_months)
            
        # 데이터프레임 표시
        st.subheader("연도별 투자 현황")
        yearly_df = df[df['월'] % 12 == 0].copy()
        yearly_df['연도'] = yearly_df['월'] // 12
        yearly_df_display = yearly_df[['연도', '투자원금', '투자수익', '총자산']].copy()
        
        # 숫자 포맷팅
        for col in ['투자원금', '투자수익', '총자산']:
            yearly_df_display[col] = yearly_df_display[col].map('{:,.0f}'.format)
            
        st.dataframe(yearly_df_display, use_container_width=True)

def calculate_future_value(initial_investment, monthly_contribution, monthly_rate, total_months):
    # 초기 투자금의 미래 가치
    initial_future_value = initial_investment * (1 + monthly_rate) ** total_months
    
    # 월 납입금의 미래 가치 (복리 적용)
    if monthly_rate == 0:
        contribution_future_value = monthly_contribution * total_months
    else:
        contribution_future_value = monthly_contribution * ((1 + monthly_rate) ** total_months - 1) / monthly_rate
    
    return initial_future_value + contribution_future_value

def calculate_present_value(future_value, monthly_contribution, monthly_rate, total_months):
    # 월 납입금의 미래 가치
    if monthly_rate == 0:
        contribution_future_value = monthly_contribution * total_months
    else:
        contribution_future_value = monthly_contribution * ((1 + monthly_rate) ** total_months - 1) / monthly_rate
    
    # 필요한 초기 투자금 계산
    required_initial_investment = (future_value - contribution_future_value) / ((1 + monthly_rate) ** total_months)
    
    return max(0, required_initial_investment)

def generate_investment_data(initial_investment, monthly_contribution, monthly_rate, total_months):
    data = []
    balance = initial_investment
    invested = initial_investment
    
    for month in range(total_months + 1):
        if month > 0:
            interest = balance * monthly_rate
            balance += interest + monthly_contribution
            invested += monthly_contribution
        
        data.append({
            '월': month,
            '투자원금': invested,
            '투자수익': balance - invested,
            '총자산': balance
        })
    
    return pd.DataFrame(data)
