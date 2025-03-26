import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # 백엔드 설정을 먼저 해줍니다
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="영업권 평가 계산기",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "개인사업자 법인전환 시 영업권 평가 계산기 | 개발: Manus"
    }
)

# 앱 제목 및 소개
st.title("개인사업자 법인전환 영업권 평가 계산기")
st.markdown("""
이 애플리케이션은 개인사업자가 법인으로 전환할 때 영업권 평가를 위한 두 가지 주요 방식(세무사 방식과 감정평가사 방식)을 
비교하고 시뮬레이션할 수 있는 도구입니다.
""")

# 사이드바 - 입력 파라미터
st.sidebar.header("입력 파라미터")

# 기본 입력 파라미터
with st.sidebar.expander("기본 정보", expanded=True):
    business_years = st.number_input("사업 운영 기간(년)", min_value=1, max_value=50, value=5)
    avg_annual_profit = st.number_input("연평균 순이익(원)", min_value=0, value=100000000, step=10000000, format="%d")
    future_growth_rate = st.slider("향후 성장률 예상(%)", min_value=-20, max_value=50, value=10, step=1)

# 세무사 방식 파라미터
with st.sidebar.expander("세무사 방식 파라미터", expanded=True):
    tax_accountant_multiplier = st.slider("세무사 방식 승수(배수)", min_value=1.0, max_value=10.0, value=3.0, step=0.1)
    
# 감정평가사 방식 파라미터
with st.sidebar.expander("감정평가사 방식 파라미터", expanded=True):
    forecast_years = st.slider("미래 예측 기간(년)", min_value=1, max_value=10, value=5)
    discount_rate = st.slider("할인율(%)", min_value=1, max_value=30, value=15, step=1)

# 세금 관련 파라미터
with st.sidebar.expander("세금 관련 파라미터", expanded=True):
    income_tax_rate = st.slider("개인 소득세율(%)", min_value=5, max_value=45, value=35, step=1)
    corporate_tax_rate = st.slider("법인세율(%)", min_value=5, max_value=30, value=20, step=1)
    necessary_expense_rate = st.slider("필요경비 인정률(%)", min_value=0, max_value=100, value=60, step=1)

# 계산 함수
def calculate_tax_accountant_valuation(avg_annual_profit, multiplier):
    """세무사 방식 영업권 평가액 계산"""
    return avg_annual_profit * multiplier

def calculate_appraiser_valuation(avg_annual_profit, growth_rate, forecast_years, discount_rate):
    """감정평가사 방식 영업권 평가액 계산 (DCF 방식)"""
    total_present_value = 0
    
    for year in range(1, forecast_years + 1):
        future_profit = avg_annual_profit * (1 + growth_rate/100) ** year
        present_value = future_profit / ((1 + discount_rate/100) ** year)
        total_present_value += present_value
    
    return total_present_value

def calculate_tax_impact(valuation, income_tax_rate, corporate_tax_rate, necessary_expense_rate):
    """세금 영향 계산"""
    # 개인 소득세 계산
    taxable_income = valuation * (1 - necessary_expense_rate/100)
    personal_income_tax = taxable_income * (income_tax_rate/100)
    
    # 법인 감가상각 혜택 계산 (5년 정액법)
    annual_depreciation = valuation / 5
    corporate_tax_savings = annual_depreciation * (corporate_tax_rate/100) * 5
    
    return {
        "taxable_income": taxable_income,
        "personal_income_tax": personal_income_tax,
        "annual_depreciation": annual_depreciation,
        "corporate_tax_savings": corporate_tax_savings,
        "net_tax_effect": corporate_tax_savings - personal_income_tax
    }

# 계산 실행
tax_accountant_valuation = calculate_tax_accountant_valuation(avg_annual_profit, tax_accountant_multiplier)
appraiser_valuation = calculate_appraiser_valuation(avg_annual_profit, future_growth_rate, forecast_years, discount_rate)

# 세금 영향 계산
tax_accountant_tax_impact = calculate_tax_impact(tax_accountant_valuation, income_tax_rate, corporate_tax_rate, necessary_expense_rate)
appraiser_tax_impact = calculate_tax_impact(appraiser_valuation, income_tax_rate, corporate_tax_rate, necessary_expense_rate)

# 결과 표시
st.header("영업권 평가 결과")

col1, col2 = st.columns(2)

with col1:
    st.subheader("세무사 방식")
    st.metric("평가액", f"{tax_accountant_valuation:,.0f}원")
    st.write(f"계산 방법: {avg_annual_profit:,.0f}원 × {tax_accountant_multiplier}배")
    
    st.markdown("### 세금 영향")
    st.write(f"과세대상 소득: {tax_accountant_tax_impact['taxable_income']:,.0f}원")
    st.write(f"개인 소득세: {tax_accountant_tax_impact['personal_income_tax']:,.0f}원")
    st.write(f"연간 감가상각비: {tax_accountant_tax_impact['annual_depreciation']:,.0f}원")
    st.write(f"법인세 절감액(5년): {tax_accountant_tax_impact['corporate_tax_savings']:,.0f}원")
    st.metric("순 세금 효과", f"{tax_accountant_tax_impact['net_tax_effect']:,.0f}원")

with col2:
    st.subheader("감정평가사 방식")
    st.metric("평가액", f"{appraiser_valuation:,.0f}원")
    st.write(f"계산 방법: DCF(할인율 {discount_rate}%, 성장률 {future_growth_rate}%, {forecast_years}년)")
    
    st.markdown("### 세금 영향")
    st.write(f"과세대상 소득: {appraiser_tax_impact['taxable_income']:,.0f}원")
    st.write(f"개인 소득세: {appraiser_tax_impact['personal_income_tax']:,.0f}원")
    st.write(f"연간 감가상각비: {appraiser_tax_impact['annual_depreciation']:,.0f}원")
    st.write(f"법인세 절감액(5년): {appraiser_tax_impact['corporate_tax_savings']:,.0f}원")
    st.metric("순 세금 효과", f"{appraiser_tax_impact['net_tax_effect']:,.0f}원")

# 비교 시각화
st.header("방식별 비교")

# 평가액 비교 차트
fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=['세무사 방식', '감정평가사 방식'],
    y=[tax_accountant_valuation, appraiser_valuation],
    text=[f"{tax_accountant_valuation:,.0f}원", f"{appraiser_valuation:,.0f}원"],
    textposition='auto',
    marker_color=['#1f77b4', '#ff7f0e']
))
fig1.update_layout(
    title='영업권 평가액 비교',
    xaxis_title='평가 방식',
    yaxis_title='평가액(원)',
    height=500
)
st.plotly_chart(fig1, use_container_width=True)

# 세금 효과 비교 차트
fig2 = make_subplots(rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]],
                    subplot_titles=("세무사 방식 세금 효과", "감정평가사 방식 세금 효과"))

fig2.add_trace(go.Pie(
    labels=['개인 소득세', '법인세 절감액'],
    values=[tax_accountant_tax_impact['personal_income_tax'], tax_accountant_tax_impact['corporate_tax_savings']],
    marker_colors=['#d62728', '#2ca02c'],
    name="세무사 방식"
), row=1, col=1)

fig2.add_trace(go.Pie(
    labels=['개인 소득세', '법인세 절감액'],
    values=[appraiser_tax_impact['personal_income_tax'], appraiser_tax_impact['corporate_tax_savings']],
    marker_colors=['#d62728', '#2ca02c'],
    name="감정평가사 방식"
), row=1, col=2)

fig2.update_layout(height=500)
st.plotly_chart(fig2, use_container_width=True)

# 방식별 특징 비교
st.header("방식별 특징 비교")

comparison_data = {
    "구분": ["법적 근거", "평가 기준", "평가 금액", "공신력", "소득처리"],
    "세무사 방식": [
        "상속세 및 증여세법(보충적 평가 방법)",
        "과거 3년간 실적 기반 순이익 할인",
        "역사적 실적 반영으로 상대적 저평가",
        "세무조사 시 부당행위계산 부인 리스크",
        "기타소득 60% 필요경비 인정"
    ],
    "감정평가사 방식": [
        "법인세법 제89조 제2항 제1호",
        "미래 3~5년 예상 수익 현가할인",
        "성장 전망 반영으로 고평가 가능",
        "세무당국이 공식 인정하는 방식",
        "동일 적용(법인측 5년 감가상각)"
    ]
}

comparison_df = pd.DataFrame(comparison_data)
st.table(comparison_df)

# 방식 선택 시 고려사항
st.header("방식 선택 시 고려사항")

st.markdown("""
1. **세금절감 효과**  
   감정평가 방식으로 평가액이 높을 경우 개인은 필요경비로 더 많은 공제를 받을 수 있으며, 
   법인은 더 큰 감가상각 혜택을 받을 수 있습니다.

2. **법적 안정성**  
   감정평가서 미제출 시 세무조사 대상이 될 가능성이 높으며, 
   평가액 차이가 크게 발생할 경우 부당행위계산 부인 가능성이 있습니다.

3. **비용 대비 효과**  
   감정평가 수수료(평가액의 0.3~1%)가 추가되나, 
   평가액이 높을수록 세금 절감 효과가 커져 경제성이 확보됩니다.
""")

# 면책 조항
st.markdown("---")
st.caption("""
**면책 조항**: 이 계산기는 교육 및 참고용으로만 제공됩니다. 실제 영업권 평가 및 세금 계산은 전문가와 상담하시기 바랍니다.
""")
