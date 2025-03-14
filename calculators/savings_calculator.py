import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def calculate_simple_interest(principal, rate, time):
    """단리 계산 함수"""
    interest = principal * (rate/100) * time
    total_amount = principal + interest
    return total_amount, interest

def calculate_compound_interest(principal, rate, time, compounds_per_year=1):
    """복리 계산 함수"""
    n = compounds_per_year  # 연간 복리 횟수
    r = rate / 100  # 비율로 변환
    amount = principal * (1 + r/n)**(n*time)
    interest = amount - principal
    return amount, interest

def get_compound_freq_name(compounds_per_year):
    """복리 주기 이름 반환"""
    compound_dict = {
        1: "연복리", 
        2: "반기복리", 
        4: "분기복리", 
        12: "월복리", 
        365: "일복리"
    }
    return compound_dict.get(compounds_per_year, f"{compounds_per_year}회 복리")

def yearly_growth_data(principal, rate, time, compounds_per_year=1, is_compound=True):
    """연도별 성장 데이터 계산"""
    data = []
    
    for year in range(int(time) + 1):
        if year == 0:
            data.append({"연도": year, "금액": principal, "이자": 0})
        else:
            if is_compound:
                # 복리 계산
                amount, interest = calculate_compound_interest(
                    principal, rate, year, compounds_per_year
                )
                total_interest = amount - principal
            else:
                # 단리 계산
                amount, total_interest = calculate_simple_interest(principal, rate, year)
            
            yearly_interest = total_interest / year
            data.append({"연도": year, "금액": amount, "이자": yearly_interest})
    
    return pd.DataFrame(data)

def format_number(number):
    """숫자에 콤마 추가"""
    return f"{number:,}"

def parse_input_number(text):
    """입력 텍스트에서 콤마 제거하고 숫자 변환"""
    if not text:
        return 0
    return int(text.replace(",", ""))

def savings_calculator_tab():
    st.header("예적금 계산기 💰")
    
    # 계산 모드 선택 (단리/복리 비교 또는 예금/적금 비교)
    calc_mode = st.radio(
        "계산 모드 선택", 
        ["단리/복리 비교", "예금/적금 비교"],
        horizontal=True
    )
    
    if calc_mode == "단리/복리 비교":
        simple_compound_calculator()
    else:
        deposit_installment_calculator()

def simple_compound_calculator():
    """단리/복리 비교 계산기"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("입력 정보")
        
        # 원금 입력 (콤마 표시)
        principal_text = st.text_input(
            "원금 (원)", 
            value="10,000,000",
            help="원금을 입력하세요. 콤마(,)는 자동으로 처리됩니다."
        )
        principal = parse_input_number(principal_text)
        
        interest_rate = st.number_input("연이율 (%)", min_value=0.1, max_value=20.0, value=3.0, step=0.1)
        investment_period = st.number_input("투자 기간 (년)", min_value=0.5, max_value=50.0, value=5.0, step=0.5)
        
        compound_period = st.selectbox(
            "복리 계산 주기", 
            options=[1, 2, 4, 12, 365],
            format_func=get_compound_freq_name,
            index=0
        )
        
        # 계산하기 버튼
        calculate_button = st.button("계산하기", key="simple_compound_calc")
    
    # 상태 초기화
    if 'simple_result' not in st.session_state:
        st.session_state.simple_result = None
    if 'compound_result' not in st.session_state:
        st.session_state.compound_result = None
    if 'simple_data' not in st.session_state:
        st.session_state.simple_data = None
    if 'compound_data' not in st.session_state:
        st.session_state.compound_data = None
    
    # 계산 수행
    if calculate_button:
        # 단리 계산
        simple_amount, simple_interest = calculate_simple_interest(principal, interest_rate, investment_period)
        # 복리 계산
        compound_amount, compound_interest = calculate_compound_interest(
            principal, interest_rate, investment_period, compound_period
        )
        
        # 결과 저장
        st.session_state.simple_result = (simple_amount, simple_interest)
        st.session_state.compound_result = (compound_amount, compound_interest)
        
        # 데이터 준비
        st.session_state.simple_data = yearly_growth_data(principal, interest_rate, investment_period, is_compound=False)
        st.session_state.compound_data = yearly_growth_data(principal, interest_rate, investment_period, compound_period, is_compound=True)
    
    with col2:
        st.subheader("결과 비교")
        
        if st.session_state.simple_result and st.session_state.compound_result:
            simple_amount, simple_interest = st.session_state.simple_result
            compound_amount, compound_interest = st.session_state.compound_result
            
            col_simple, col_compound = st.columns(2)
            
            with col_simple:
                st.markdown("#### 단리")
                st.metric("최종 금액", f"{simple_amount:,.0f}원")
                st.metric("총 이자", f"{simple_interest:,.0f}원")
                st.metric("이자 비율", f"{(simple_interest/principal)*100:.2f}%")
            
            with col_compound:
                st.markdown(f"#### 복리 ({get_compound_freq_name(compound_period)})")
                st.metric("최종 금액", f"{compound_amount:,.0f}원")
                st.metric("총 이자", f"{compound_interest:,.0f}원") 
                st.metric("이자 비율", f"{(compound_interest/principal)*100:.2f}%")
            
            difference = compound_amount - simple_amount
            st.info(f"복리가 단리보다 **{difference:,.0f}원** 더 많은 수익을 냅니다. (차이: {(difference/simple_amount*100):.2f}%)")
        else:
            st.info("입력 정보를 입력한 후 '계산하기' 버튼을 클릭하세요.")
    
    # 계산 결과가 있을 때만 그래프 표시
    if st.session_state.simple_data is not None and st.session_state.compound_data is not None:
        # 그래프 탭
        st.subheader("연도별 비교")
        tab1, tab2, tab3 = st.tabs(["금액 비교", "연간 이자", "데이터"])
        
        with tab1:
            fig = go.Figure()
            
            # 원금 선 추가
            fig.add_trace(go.Scatter(
                x=st.session_state.simple_data['연도'], 
                y=[principal] * len(st.session_state.simple_data),
                mode='lines',
                name='원금',
                line=dict(color='gray', dash='dash')
            ))
            
            # 단리 선 추가
            fig.add_trace(go.Scatter(
                x=st.session_state.simple_data['연도'], 
                y=st.session_state.simple_data['금액'],
                mode='lines+markers',
                name='단리',
                line=dict(color='blue')
            ))
            
            # 복리 선 추가
            fig.add_trace(go.Scatter(
                x=st.session_state.compound_data['연도'], 
                y=st.session_state.compound_data['금액'],
                mode='lines+markers',
                name=f'복리 ({get_compound_freq_name(compound_period)})',
                line=dict(color='red')
            ))
            
            fig.update_layout(
                title='단리 vs 복리 금액 비교',
                xaxis_title='연도',
                yaxis_title='금액 (원)',
                legend=dict(y=0.99, x=0.01),
                template='seaborn'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 그래프 설명 추가
            st.markdown("""
            **그래프 설명:**
            - **회색 점선**: 초기 투자한 원금을 나타냅니다. 시간이 지나도 변하지 않습니다.
            - **파란색 선**: 단리로 계산된 금액입니다. 원금에 대해서만 이자가 붙기 때문에 일정한 기울기로 증가합니다.
            - **빨간색 선**: 복리로 계산된 금액입니다. 원금과 이전 이자에 대해 이자가 붙기 때문에 시간이 지날수록 증가율이 커집니다.
            
            투자 기간이 길어질수록 단리와 복리의 차이가 더 커지는 것을 볼 수 있습니다. 이것이 장기 투자에서 복리의 중요성을 보여주는 이유입니다.
            """)
            
        with tab2:
            fig = go.Figure()
            
            # 단리 이자 막대 추가
            fig.add_trace(go.Bar(
                x=st.session_state.simple_data['연도'][1:], 
                y=st.session_state.simple_data['이자'][1:],
                name='단리',
                marker_color='blue'
            ))
            
            # 복리 이자 막대 추가
            fig.add_trace(go.Bar(
                x=st.session_state.compound_data['연도'][1:], 
                y=st.session_state.compound_data['이자'][1:],
                name=f'복리 ({get_compound_freq_name(compound_period)})',
                marker_color='red'
            ))
            
            fig.update_layout(
                title='연간 이자 비교',
                xaxis_title='연도',
                yaxis_title='연간 이자 (원)',
                barmode='group',
                template='seaborn'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # 그래프 설명 추가
            st.markdown("""
            **그래프 설명:**
            - **파란색 막대**: 각 연도에 단리로 발생하는 이자입니다. 매년 동일한 금액의 이자가 발생합니다.
            - **빨간색 막대**: 각 연도에 복리로 발생하는 이자입니다. 시간이 지날수록 이자 금액이 증가합니다.
            
            복리의 경우 시간이 지날수록 이자 금액이 계속 증가하는 반면, 단리는 매년 동일한 이자가 발생합니다.
            """)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 단리 상세 데이터")
                st.dataframe(st.session_state.simple_data.style.format({
                    "금액": "{:,.0f}원", 
                    "이자": "{:,.0f}원"
                }))
            
            with col2:
                st.markdown(f"#### 복리 상세 데이터 ({get_compound_freq_name(compound_period)})")
                st.dataframe(st.session_state.compound_data.style.format({
                    "금액": "{:,.0f}원", 
                    "이자": "{:,.0f}원"
                }))
    
    # 사용법 안내
    st.subheader("사용 방법")
    st.markdown("""
    1. **입력 정보**에 원금, 연이율, 투자 기간을 입력하세요.
    2. 복리 계산 주기를 선택하세요 (연복리, 반기복리, 분기복리, 월복리, 일복리).
    3. **계산하기** 버튼을 클릭하세요.
    4. **결과 비교**에서 단리와 복리의 최종 금액과 이자를 확인하세요.
    5. **연도별 비교** 탭에서 시간에 따른 금액 변화를 그래프로 확인하세요.
    """)
    
    # 추가 정보 확장 섹션
    with st.expander("단리와 복리의 차이"):
        st.markdown("""
        ### 단리 (Simple Interest)
        - 원금에 대해서만 이자가 계산됩니다.
        - 계산식: 원금 × 이율 × 기간
        - 시간이 지나도 이자는 선형적으로 증가합니다.
        
        ### 복리 (Compound Interest)
        - 원금뿐만 아니라 이전에 발생한 이자에 대해서도 이자가 계산됩니다.
        - 계산식: 원금 × (1 + 이율/복리횟수)^(복리횟수×기간)
        - 시간이 지날수록 이자가 기하급수적으로 증가합니다.
        - 복리 계산 주기가 짧을수록(연복리보다 월복리, 월복리보다 일복리) 더 많은 이자가 발생합니다.
        
        ### 알버트 아인슈타인의 명언
        > "복리는 세상에서 8번째 불가사의다."
        
        장기 투자에서는 복리의 효과가 매우 크게 나타납니다. 시간이 지날수록 단리와 복리의 차이는 더욱 벌어집니다.
        """)

def deposit_installment_calculator():
    """예금/적금 비교 계산기"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("입력 정보")
        
        # 예금 원금 입력 (콤마 표시)
        principal_text = st.text_input(
            "예금 원금 (원)", 
            value="10,000,000",
            help="예금은 한 번에 맡기는 목돈입니다. 콤마(,)는 자동으로 처리됩니다."
        )
        principal = parse_input_number(principal_text)
        
        # 적금 월 납입액 입력 (콤마 표시)
        monthly_deposit_text = st.text_input(
            "적금 월 납입액 (원)", 
            value="500,000",
            help="적금은 매월 정기적으로 납입하는 금액입니다. 콤마(,)는 자동으로 처리됩니다."
        )
        monthly_deposit = parse_input_number(monthly_deposit_text)
        
        interest_rate = st.number_input("연이율 (%)", min_value=0.1, max_value=20.0, value=3.0, step=0.1)
        investment_period = st.number_input("저축 기간 (년)", min_value=0.5, max_value=50.0, value=2.0, step=0.5)
        
        compound_period = st.selectbox(
            "복리 계산 주기", 
            options=[1, 2, 4, 12, 365],
            format_func=get_compound_freq_name,
            index=0
        )
        
        # 계산하기 버튼
        calculate_button = st.button("계산하기", key="deposit_installment_calc")
    
    # 상태 초기화
    if 'deposit_result' not in st.session_state:
        st.session_state.deposit_result = None
    if 'installment_result' not in st.session_state:
        st.session_state.installment_result = None
    if 'deposit_data' not in st.session_state:
        st.session_state.deposit_data = None
    if 'installment_data' not in st.session_state:
        st.session_state.installment_data = None
    
    # 계산 수행
    if calculate_button:
        # 예금 계산 (한 번에 목돈 예치)
        deposit_amount, deposit_interest = calculate_compound_interest(
            principal, interest_rate, investment_period, compound_period
        )
        
        # 적금 계산 (매월 납입)
        # 적금 총 납입액
        total_installment_principal = monthly_deposit * investment_period * 12
        
        # 매월 납입 시 복리 계산
        installment_amount = 0
        for month in range(int(investment_period * 12)):
            remaining_time = investment_period - (month / 12)
            amount, _ = calculate_compound_interest(
                monthly_deposit, interest_rate, remaining_time, 12
            )
            installment_amount += amount
        
        installment_interest = installment_amount - total_installment_principal
        
        # 결과 저장
        st.session_state.deposit_result = (deposit_amount, deposit_interest)
        st.session_state.installment_result = (installment_amount, installment_interest, total_installment_principal)
        
        # 차트 데이터 준비
        years = np.arange(0, investment_period + 0.1, 0.25)
        deposit_values = []
        installment_values = []
        installment_principals = []
        
        for year in years:
            # 예금 계산
            deposit_value, _ = calculate_compound_interest(principal, interest_rate, year, compound_period)
            deposit_values.append(deposit_value)
            
            # 적금 계산
            months = int(year * 12)
            installment_principal = monthly_deposit * months
            installment_principals.append(installment_principal)
            
            # 매월 납입 시 복리 계산
            installment_value = 0
            for m in range(months):
                remaining_time = year - (m / 12)
                if remaining_time > 0:
                    amount, _ = calculate_compound_interest(monthly_deposit, interest_rate, remaining_time, 12)
                    installment_value += amount
            
            installment_values.append(installment_value)
        
        # 데이터 저장
        st.session_state.deposit_data = {
            'years': years,
            'values': deposit_values
        }
        st.session_state.installment_data = {
            'years': years,
            'values': installment_values,
            'principals': installment_principals
        }
    
    with col2:
        st.subheader("결과 비교")
        
        if st.session_state.deposit_result and st.session_state.installment_result:
            deposit_amount, deposit_interest = st.session_state.deposit_result
            installment_amount, installment_interest, total_installment_principal = st.session_state.installment_result
            
            col_deposit, col_installment = st.columns(2)
            
            with col_deposit:
                st.markdown("#### 예금 (목돈 예치)")
                st.metric("최종 금액", f"{deposit_amount:,.0f}원")
                st.metric("총 이자", f"{deposit_interest:,.0f}원")
                st.metric("원금", f"{principal:,.0f}원")
                st.metric("이자 비율", f"{(deposit_interest/principal)*100:.2f}%")
            
            with col_installment:
                st.markdown("#### 적금 (월 납입)")
                st.metric("최종 금액", f"{installment_amount:,.0f}원")
                st.metric("총 이자", f"{installment_interest:,.0f}원")
                st.metric("총 납입액", f"{total_installment_principal:,.0f}원")
                st.metric("이자 비율", f"{(installment_interest/total_installment_principal)*100:.2f}%")
            
            if deposit_amount > installment_amount:
                difference = deposit_amount - installment_amount
                st.info(f"예금이 적금보다 **{difference:,.0f}원** 더 많은 수익을 냅니다. (차이: {(difference/installment_amount*100):.2f}%)")
            else:
                difference = installment_amount - deposit_amount
                st.info(f"적금이 예금보다 **{difference:,.0f}원** 더 많은 수익을 냅니다. (차이: {(difference/deposit_amount*100):.2f}%)")
        else:
            st.info("입력 정보를 입력한 후 '계산하기' 버튼을 클릭하세요.")
    
    # 차트 표시
    if st.session_state.deposit_data and st.session_state.installment_data:
        st.subheader("연도별 비교")
        
        fig = go.Figure()
        
        # 예금 원금 선 추가
        fig.add_trace(go.Scatter(
            x=st.session_state.deposit_data['years'], 
            y=[principal] * len(st.session_state.deposit_data['years']),
            mode='lines',
            name='예금 원금',
            line=dict(color='gray', dash='dash')
        ))
        
        # 예금 금액 선 추가
        fig.add_trace(go.Scatter(
            x=st.session_state.deposit_data['years'], 
            y=st.session_state.deposit_data['values'],
            mode='lines',
            name='예금 금액',
            line=dict(color='blue')
        ))
        
        # 적금 납입액 선 추가
        fig.add_trace(go.Scatter(
            x=st.session_state.installment_data['years'], 
            y=st.session_state.installment_data['principals'],
            mode='lines',
            name='적금 납입액',
            line=dict(color='green', dash='dash')
        ))
        
        # 적금 금액 선 추가
        fig.add_trace(go.Scatter(
            x=st.session_state.installment_data['years'], 
            y=st.session_state.installment_data['values'],
            mode='lines',
            name='적금 금액',
            line=dict(color='red')
        ))
        
        fig.update_layout(
            title='예금 vs 적금 금액 비교',
            xaxis_title='년',
            yaxis_title='금액 (원)',
            legend=dict(y=0.99, x=0.01),
            template='seaborn'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 그래프 설명 추가
        st.markdown("""
        **그래프 설명:**
        - **회색 점선**: 처음에 한 번에 예치한 예금 원금입니다. 시간이 지나도 변하지 않습니다.
        - **파란색 선**: 예금 원금에 이자가 붙어서 증가하는 예금 금액입니다.
        - **초록색 점선**: 매월 납입하는 적금의 납입액 합계입니다. 시간이 지날수록 선형적으로 증가합니다.
        - **빨간색 선**: 적금 납입액에 이자가 붙어서 증가하는 적금 총액입니다.
        
        예금은 처음부터 목돈에 이자가 붙지만, 적금은 납입액이 점점 쌓이면서 이자도 함께 증가합니다.
        일반적으로 총 투자금액이 같다면 예금이 더 유리하지만, 현실에서는 적금의 이율이 예금보다 높은 경우가 많습니다.
        """)
    
    # 사용법 안내
    st.subheader("사용 방법")
    st.markdown("""
    1. **입력 정보**에 예금 원금, 적금 월 납입액, 연이율, 저축 기간을 입력하세요.
    2. **계산하기** 버튼을 클릭하세요.
    3. **결과 비교**에서 예금과 적금의 최종 금액과 이자를 확인하세요.
    4. 그래프에서 시간에 따른 각 저축 방식의 금액 변화를 확인하세요.
    """)
    
    # 추가 정보 확장 섹션
    with st.expander("예금과 적금의 차이"):
        st.markdown("""
        ### 예금 (Deposit)
        - 목돈을 한 번에 맡기는 방식입니다.
        - 시작부터 전체 원금에 대해 이자가 발생합니다.
        - 중도 인출이 상대적으로 자유로운 경우가 많습니다.
        - 이미 목돈이 있는 경우 유리합니다.
        
        ### 적금 (Installment Savings)
        - 일정 금액을 정기적으로 나눠서 납입하는 방식입니다.
        - 납입한 금액에 대해서만 이자가 발생합니다.
        - 저축 습관을 들이는 데 도움이 됩니다.
        - 목돈을 모으는 과정에 적합합니다.
        
        ### 비교
        예금과 적금을 비교할 때는 다음 사항을 고려하세요:
        - 총 투자금액이 같다면 예금이 더 유리합니다 (시작부터 전체 금액에 이자가 붙기 때문).
        - 실제로는 적금의 이율이 예금보다 높은 경우가 많습니다.
        - 목표 금액을 모으는 것이 중요하다면, 자신의 저축 습관을 고려하여 선택하세요.
        """)

# 직접 실행 시 테스트용
if __name__ == "__main__":
    st.set_page_config(page_title="예적금 계산기", layout="wide")
    savings_calculator_tab()
