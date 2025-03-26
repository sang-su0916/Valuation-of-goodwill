import streamlit as st
import pandas as pd
import numpy as np

def investment_calculator():
    st.header("투자계산기")
    
    # 사용 방법 안내
    with st.expander("💡 투자계산기 사용 방법"):
        st.write("""
        이 투자계산기는 두 가지 핵심 계산을 제공합니다:
        
        **미래가치(FV) 계산**: 현재 투자금액이 미래에 얼마가 될지 계산합니다.
        - 예: 현재 1천만원과 매월 50만원을 연 7%로 10년간 투자하면 얼마가 될까요?
        
        **현재가치(PV) 계산**: 미래에 필요한 금액을 위해 현재 얼마를 투자해야 할지 계산합니다.
        - 예: 10년 후 1억원이 필요하다면, 연 7%로 투자할 때 현재 얼마를 준비해야 할까요?
        """)
    
    # 계산 유형 선택
    calc_type = st.radio(
        "계산 유형",
        options=["미래가치(FV) 계산", "현재가치(PV) 계산"],
        horizontal=True
    )
    
    tabs = st.tabs(["기본 입력", "상세 설정"])
    
    with tabs[0]:
        col1, col2 = st.columns(2)
        
        with col1:
            if calc_type == "미래가치(FV) 계산":
                initial_investment_text = st.text_input(
                    "초기투자금액 (원)",
                    value="10,000,000",
                    help="처음에 한 번 투자하는 금액",
                    key="initial_investment_fv"
                )
                try:
                    initial_investment = int(initial_investment_text.replace(',', ''))
                except:
                    initial_investment = 10000000
            else:
                target_amount_text = st.text_input(
                    "목표금액 (원)",
                    value="100,000,000",
                    help="미래에 달성하고자 하는 목표 금액",
                    key="target_amount_pv"
                )
                try:
                    target_amount = int(target_amount_text.replace(',', ''))
                except:
                    target_amount = 100000000
                
            monthly_contribution_text = st.text_input(
                "정기 투자금액 (원)",
                value="500,000",
                help="정기적으로 추가 투자하는 금액",
                key="monthly_contribution"
            )
            try:
                monthly_contribution = int(monthly_contribution_text.replace(',', ''))
            except:
                monthly_contribution = 500000
            
            # 정기 투자 주기 선택
            contribution_period = st.radio(
                "투자 주기",
                options=["월 납입", "연 납입"],
                horizontal=True,
                index=0
            )
        
        with col2:
            # 투자 기간 단위 선택
            period_unit = st.radio(
                "투자 기간 단위",
                options=["년", "월"],
                horizontal=True,
                index=0
            )
            
            if period_unit == "년":
                investment_period = st.number_input(
                    "투자기간 (년)",
                    min_value=1,
                    max_value=50,
                    value=10
                )
                total_months = investment_period * 12
            else:
                investment_period = st.number_input(
                    "투자기간 (월)",
                    min_value=1,
                    max_value=600,
                    value=120
                )
                total_months = investment_period
            
            # 이율 단위 선택
            rate_unit = st.radio(
                "수익률 단위",
                options=["연이율", "월이율"],
                horizontal=True,
                index=0
            )
            
            if rate_unit == "연이율":
                annual_return = st.number_input(
                    "연수익률 (%)",
                    min_value=0.0,
                    max_value=30.0,
                    value=7.0,
                    step=0.5
                )
                monthly_rate = annual_return / 12 / 100
            else:
                monthly_return = st.number_input(
                    "월수익률 (%)",
                    min_value=0.0,
                    max_value=5.0,
                    value=0.6,
                    step=0.1
                )
                monthly_rate = monthly_return / 100
                annual_return = monthly_rate * 12 * 100
    
    with tabs[1]:
        # 복리 계산 주기 선택
        compound_freq = st.selectbox(
            "복리 계산 주기",
            options=["월 복리", "분기 복리", "반기 복리", "연 복리"],
            index=0
        )
        
        if compound_freq == "월 복리":
            compounding_periods = 12
        elif compound_freq == "분기 복리":
            compounding_periods = 4
        elif compound_freq == "반기 복리":
            compounding_periods = 2
        else:  # 연 복리
            compounding_periods = 1
    
    # 조정된 월이율 계산
    if compounding_periods < 12:
        periodic_rate = annual_return / 100 / compounding_periods
        effective_monthly_rate = (1 + periodic_rate) ** (1 / (12 / compounding_periods)) - 1
    else:
        effective_monthly_rate = monthly_rate
    
    if st.button("계산하기", key="investment_calc_button", use_container_width=True):
        # 투자 주기에 따른 기여금 조정
        if contribution_period == "연 납입":
            monthly_equivalent = monthly_contribution / 12
        else:
            monthly_equivalent = monthly_contribution
        
        if calc_type == "미래가치(FV) 계산":
            # 미래가치 계산
            future_value = calculate_future_value(initial_investment, monthly_equivalent, effective_monthly_rate, total_months)
            
            # 총 투자금액 계산
            if contribution_period == "월 납입":
                total_contributions = initial_investment + monthly_contribution * total_months
            else:  # 연 납입
                total_contributions = initial_investment + monthly_contribution * (total_months / 12)
                
            investment_gain = future_value - total_contributions
            
            # 결과 표시
            st.subheader("투자 결과")
            col1, col2, col3 = st.columns(3)
            col1.metric("미래 가치", f"₩{future_value:,.0f}")
            col2.metric("총 투자금액", f"₩{total_contributions:,.0f}")
            col3.metric("투자 수익", f"₩{investment_gain:,.0f}", f"{investment_gain/total_contributions*100:.1f}%")
            
            # 결과 데이터
            df = generate_investment_data(initial_investment, monthly_equivalent, effective_monthly_rate, total_months, contribution_period)
            
            # 표시 간격 선택
            display_interval = st.selectbox(
                "표시 간격",
                options=["연도별", "월별", "분기별"],
                index=0
            )
            
            if display_interval == "연도별":
                display_df = df[df['월'] % 12 == 0].copy()
                display_df['기간'] = display_df['월'] // 12
                display_df['단위'] = "년"
            elif display_interval == "분기별":
                display_df = df[df['월'] % 3 == 0].copy()
                display_df['기간'] = display_df['월'] // 3
                display_df['단위'] = "분기"
            else:  # 월별
                display_df = df.copy()
                display_df['기간'] = display_df['월']
                display_df['단위'] = "월"
            
            display_df = display_df[['기간', '단위', '투자원금', '투자수익', '총자산']].copy()
            
            # 숫자 포맷팅
            for col in ['투자원금', '투자수익', '총자산']:
                display_df[col] = display_df[col].map('{:,.0f}'.format)
                
            st.dataframe(display_df, use_container_width=True)
            
        else:  # 현재가치(PV) 계산
            # 현재가치 계산
            present_value = calculate_present_value(target_amount, monthly_equivalent, effective_monthly_rate, total_months)
            
            # 총 기여금 계산
            if contribution_period == "월 납입":
                total_contributions = monthly_contribution * total_months
            else:  # 연 납입
                total_contributions = monthly_contribution * (total_months / 12)
                
            total_required = present_value + total_contributions
            future_gain = target_amount - total_required
            
            # 결과 표시
            st.subheader("투자 결과")
            col1, col2, col3 = st.columns(3)
            col1.metric("필요 초기 투자금", f"₩{present_value:,.0f}")
            col2.metric("총 정기 투자액", f"₩{total_contributions:,.0f}")
            col3.metric("투자 수익", f"₩{future_gain:,.0f}", f"{future_gain/total_required*100:.1f}%")
            
            # 결과 데이터
            df = generate_investment_data(present_value, monthly_equivalent, effective_monthly_rate, total_months, contribution_period)
            
            # 표시 간격 선택
            display_interval = st.selectbox(
                "표시 간격",
                options=["연도별", "월별", "분기별"],
                index=0
            )
            
            if display_interval == "연도별":
                display_df = df[df['월'] % 12 == 0].copy()
                display_df['기간'] = display_df['월'] // 12
                display_df['단위'] = "년"
            elif display_interval == "분기별":
                display_df = df[df['월'] % 3 == 0].copy()
                display_df['기간'] = display_df['월'] // 3
                display_df['단위'] = "분기"
            else:  # 월별
                display_df = df.copy()
                display_df['기간'] = display_df['월']
                display_df['단위'] = "월"
            
            display_df = display_df[['기간', '단위', '투자원금', '투자수익', '총자산']].copy()
            
            # 숫자 포맷팅
            for col in ['투자원금', '투자수익', '총자산']:
                display_df[col] = display_df[col].map('{:,.0f}'.format)
                
            st.dataframe(display_df, use_container_width=True)

def calculate_future_value(initial_investment, monthly_contribution, monthly_rate, total_months):
    """미래 자금을 계산합니다."""
    # 현재 저축의 성장
    future_savings = initial_investment * (1 + monthly_rate) ** total_months
    
    # 월 저축의 성장 (복리 적용)
    if monthly_rate > 0:
        future_contributions = monthly_contribution * ((1 + monthly_rate) ** total_months - 1) / monthly_rate
    else:
        future_contributions = monthly_contribution * total_months
    
    return future_savings + future_contributions

def calculate_present_value(future_value, monthly_contribution, monthly_rate, total_months):
    """필요한 초기 투자금을 계산합니다."""
    # 월 납입금의 미래 가치
    if monthly_rate > 0:
        contribution_future_value = monthly_contribution * ((1 + monthly_rate) ** total_months - 1) / monthly_rate
    else:
        contribution_future_value = monthly_contribution * total_months
    
    # 필요한 초기 투자금 계산
    required_initial_investment = (future_value - contribution_future_value) / ((1 + monthly_rate) ** total_months)
    
    return max(0, required_initial_investment)

def generate_investment_data(initial_investment, monthly_contribution, monthly_rate, total_months, contribution_period):
    """투자 성장 데이터를 생성합니다."""
    data = []
    balance = initial_investment
    invested = initial_investment
    
    for month in range(total_months + 1):
        if month > 0:
            # 이자 계산
            interest = balance * monthly_rate
            
            # 월 납입인 경우 매월 추가, 연 납입인 경우 매년 시작시 추가
            if contribution_period == "월 납입" or (contribution_period == "연 납입" and month % 12 == 1):
                # 연 납입인 경우 한 번에 12개월치 추가
                contribution = monthly_contribution if contribution_period == "월 납입" else monthly_contribution * 12
                balance += interest + contribution
                invested += contribution
            else:
                balance += interest
        
        data.append({
            '월': month,
            '투자원금': invested,
            '투자수익': balance - invested,
            '총자산': balance
        })
    
    return pd.DataFrame(data)
