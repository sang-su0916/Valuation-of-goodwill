import streamlit as st
import sys
import os

# 현재 디렉토리 경로를 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 이제 calculators 모듈을 임포트할 수 있습니다
from calculators.loan_calculator import loan_calculator
from calculators.investment_calculator import investment_calculator
from calculators.retirement_calculator import retirement_calculator
from calculators.insurance_calculator import insurance_calculator

st.set_page_config(
    page_title="종합 재무계산기",
    page_icon="💰",
    layout="wide",  # 화면을 더 넓게
    initial_sidebar_state="auto"
)

def main():
    st.title("종합 재무계산기 💰")

    tabs = st.tabs(["대출계산기", "투자계산기", "은퇴계산기", "보장계산기"])

    with tabs[0]:
        loan_calculator()

    with tabs[1]:
        investment_calculator()

    with tabs[2]:
        retirement_calculator()

    with tabs[3]:
        insurance_calculator()

if __name__ == "__main__":
    main()
