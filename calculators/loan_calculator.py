import streamlit as st
import pandas as pd
import numpy as np
from utils.visualization import create_loan_payment_chart
from utils.financial_utils import calculate_loan_schedule

def format_number(number):
    return f"{number:,.0f}"

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

    if st.button("계산하기", key="loan_calc_button", use_container_width=True):
        monthly_rate = interest_rate / 12 / 100
        periods = loan_term * 12

        schedule_df = calculate_loan_schedule(
            loan_amount, periods, monthly_rate, payment_type
        )

        # 결과 섹션을 전체 너비로 표시
        st.subheader("상환 스케줄")

        # 데이터프레임 숫자 포맷팅
        formatted_df = schedule_df.copy()
        for col in ['납입금액', '원금상환', '이자금액', '잔금']:
            formatted_df[col] = formatted_df[col].map('{:,.0f}'.format)

        st.dataframe(formatted_df, use_container_width=True)

        # 그래프를 전체 너비로 표시
        fig = create_loan_payment_chart(schedule_df)
        st.plotly_chart(fig, use_container_width=True)

        total_interest = schedule_df['이자금액'].sum()
        st.info(f"총 이자금액: ₩{total_interest:,.0f}")
