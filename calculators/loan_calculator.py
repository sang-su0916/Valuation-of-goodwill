import streamlit as st
import pandas as pd
import numpy as np

def loan_calculator():
    st.header("대출계산기")

    # 입력 섹션을 위쪽에 배치
    input_col1, input_col2 = st.columns([1, 1])

    with input_col1:
        # 대출금액 입력
        loan_amount_text = st.text_input(
            "대출금액 (원)",
            value="100,000,000",
            help="숫자만 입력하세요. 예: 100000000"
        )
        try:
            loan_amount = int(loan_amount_text.replace(',', ''))
        except:
            loan_amount = 100000000

        loan_term = st.number_input("대출기간 (년)", min_value=1, value=30)

    with input_col2:
        interest_rate = st.number_input(
            "연이자율 (%)",
            min_value=0.0,
            value=3.0,
            step=0.1,
            format="%.1f"
        )
        payment_type = st.selectbox(
            "상환방식",
            ["원리금균등상환", "원금균등상환", "만기일시상환"]
        )

    if st.button("계산하기", key="loan_button", use_container_width=True):
        monthly_rate = interest_rate / 12 / 100
        periods = loan_term * 12

        # 대출 상환 스케줄 계산
        schedule = []
        remaining = loan_amount
        
        if payment_type == "원리금균등상환":
            # 원리금균등상환 - 매달 동일한 금액 납부
            if monthly_rate == 0:
                payment = loan_amount / periods
            else:
                payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** periods) / ((1 + monthly_rate) ** periods - 1)
            
            for period in range(1, periods + 1):
                interest = remaining * monthly_rate
                principal_payment = payment - interest
                remaining -= principal_payment
                
                # 마지막 회차에는 반올림 오차로 인해 잔액이 음수가 될 수 있음
                if period == periods:
                    if abs(remaining) < 1:  # 1원 미만이면 0으로 조정
                        remaining = 0
                
                schedule.append({
                    "회차": period,
                    "납입금액": payment,
                    "원금상환": principal_payment,
                    "이자금액": interest,
                    "잔금": max(0, remaining)
                })
                
        elif payment_type == "원금균등상환":
            # 원금균등상환 - 매달 동일한 원금 상환
            principal_payment = loan_amount / periods
            
            for period in range(1, periods + 1):
                interest = remaining * monthly_rate
                payment = principal_payment + interest
                remaining -= principal_payment
                
                schedule.append({
                    "회차": period,
                    "납입금액": payment,
                    "원금상환": principal_payment,
                    "이자금액": interest,
                    "잔금": max(0, remaining)
                })
                
        elif payment_type == "만기일시상환":
            # 만기일시상환 - 이자만 납부하다가 마지막에 원금 상환
            for period in range(1, periods + 1):
                interest = remaining * monthly_rate
                
                if period == periods:
                    principal_payment = loan_amount
                    payment = loan_amount + interest
                    remaining = 0
                else:
                    principal_payment = 0
                    payment = interest
                
                schedule.append({
                    "회차": period,
                    "납입금액": payment,
                    "원금상환": principal_payment,
                    "이자금액": interest,
                    "잔금": remaining
                })
        
        schedule_df = pd.DataFrame(schedule).set_index("회차")

        # 결과 섹션을 전체 너비로 표시
        st.subheader("상환 스케줄")

        # 데이터프레임 숫자 포맷팅
        formatted_df = schedule_df.copy()
        for col in ['납입금액', '원금상환', '이자금액', '잔금']:
            formatted_df[col] = formatted_df[col].map('{:,.0f}'.format)

        st.dataframe(formatted_df, use_container_width=True)

        # 간단한 요약 정보
        total_payment = schedule_df['납입금액'].sum()
        total_interest = schedule_df['이자금액'].sum()
        
        st.subheader("대출 요약")
        col1, col2, col3 = st.columns(3)
        col1.metric("총 상환금액", f"₩{total_payment:,.0f}")
        col2.metric("총 이자금액", f"₩{total_interest:,.0f}")
        col3.metric("원금대비 이자율", f"{(total_interest/loan_amount)*100:.1f}%")
