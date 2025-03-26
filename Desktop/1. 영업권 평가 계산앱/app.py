import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# 페이지 기본 설정
st.set_page_config(
    page_title="영업권 평가 시스템",
    page_icon="💰",
    layout="wide"
)

# 메인 타이틀
st.title("AI 기반 영업권 평가 시스템 📊")

# 사이드바 설정
with st.sidebar:
    st.header("평가 정보 입력")
    
    # 기본 정보 입력
    company_name = st.text_input("회사명", "")
    evaluation_date = st.date_input("평가 기준일", datetime.now())
    
    # 재무 정보 입력
    st.subheader("재무 정보")
    revenue = st.number_input("매출액 (백만원)", min_value=0.0, format="%.1f")
    operating_profit = st.number_input("영업이익 (백만원)", format="%.1f")
    
    # 성장률 및 할인율 입력
    st.subheader("성장률 및 할인율")
    growth_rate = st.slider("성장률 (%)", min_value=0.0, max_value=30.0, value=5.0)
    discount_rate = st.slider("할인율 (%)", min_value=0.0, max_value=30.0, value=10.0)
    
    # 계산 버튼
    if st.button("평가 계산", type="primary"):
        st.session_state.calculate = True
    else:
        st.session_state.calculate = False

# 메인 화면
if 'calculate' in st.session_state and st.session_state.calculate:
    # 데이터 준비
    years = range(1, 6)
    revenues = [revenue * (1 + growth_rate/100)**year for year in years]
    profits = [rev * (operating_profit/revenue) for rev in revenues]
    
    # 결과 표시
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("예측 매출액")
        df_revenue = pd.DataFrame({
            '연도': [f'{year}년차' for year in years],
            '매출액': revenues
        })
        st.dataframe(df_revenue)
        
        # 매출액 차트
        fig_revenue = px.line(df_revenue, x='연도', y='매출액', 
                            title='연도별 예측 매출액')
        st.plotly_chart(fig_revenue)
    
    with col2:
        st.subheader("예측 영업이익")
        df_profit = pd.DataFrame({
            '연도': [f'{year}년차' for year in years],
            '영업이익': profits
        })
        st.dataframe(df_profit)
        
        # 영업이익 차트
        fig_profit = px.line(df_profit, x='연도', y='영업이익',
                            title='연도별 예측 영업이익')
        st.plotly_chart(fig_profit)
    
    # 영업권 가치 계산
    present_values = [profit / ((1 + discount_rate/100)**year) for year, profit in zip(years, profits)]
    goodwill_value = sum(present_values)
    
    st.metric("영업권 평가액", f"{goodwill_value:,.0f} 백만원")
    
    # 평가 요약
    st.subheader("평가 요약")
    summary_data = {
        "구분": ["회사명", "평가기준일", "매출액", "영업이익", "성장률", "할인율", "영업권 평가액"],
        "내용": [
            company_name,
            evaluation_date.strftime("%Y-%m-%d"),
            f"{revenue:,.0f} 백만원",
            f"{operating_profit:,.0f} 백만원",
            f"{growth_rate:.1f}%",
            f"{discount_rate:.1f}%",
            f"{goodwill_value:,.0f} 백만원"
        ]
    }
    st.table(pd.DataFrame(summary_data)) 