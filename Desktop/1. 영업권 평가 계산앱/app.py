import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# 페이지 기본 설정
st.set_page_config(
    page_title="영업권 평가 시스템",
    page_icon="💰",
    layout="wide"
)

# 메인 타이틀
st.title("영업권 평가 시스템 📊")

# 사이드바 설정
with st.sidebar:
    st.header("평가 정보 입력")
    
    # 기본 정보 입력
    company_name = st.text_input("회사명", "")
    evaluation_date = st.date_input("평가 기준일", datetime.now())
    
    # 재무 정보 입력
    st.subheader("재무 정보")
    revenue = st.number_input("매출액 (백만원)", min_value=0.1, value=100.0)
    operating_profit = st.number_input("영업이익 (백만원)", value=10.0)
    
    # 성장률 및 할인율 입력
    st.subheader("성장률 및 할인율")
    growth_rate = st.slider("성장률 (%)", min_value=0.1, max_value=30.0, value=5.0)
    discount_rate = st.slider("할인율 (%)", min_value=0.1, max_value=30.0, value=10.0)
    
    # 계산 버튼
    calculate = st.button("평가 계산", type="primary")

# 메인 화면
if calculate:
    try:
        # 데이터 준비
        years = range(1, 6)
        
        # 기본 모드 계산 (단순한 모델)
        revenues = []
        profits = []
        
        for year in years:
            growth_factor = (1 + growth_rate/100)**year
            year_revenue = revenue * growth_factor
            revenues.append(year_revenue)
            
            profit_margin = operating_profit/revenue if revenue > 0 else 0
            profits.append(year_revenue * profit_margin)
        
        # 결과 표시
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("예측 매출액")
            revenue_data = {
                '연도': [f'{year}년차' for year in years],
                '매출액': revenues
            }
            st.dataframe(pd.DataFrame(revenue_data))
        
        with col2:
            st.subheader("예측 영업이익")
            profit_data = {
                '연도': [f'{year}년차' for year in years],
                '영업이익': profits
            }
            st.dataframe(pd.DataFrame(profit_data))
        
        # 영업권 가치 계산
        present_values = []
        adjusted_discount_rate = max(0.1, discount_rate)
        
        for year, profit in zip(years, profits):
            discount_factor = (1 + adjusted_discount_rate/100)**year
            present_value = profit / discount_factor
            present_values.append(present_value)
        
        goodwill_value = sum(present_values)
        
        st.metric("영업권 평가액", f"{goodwill_value:,.0f} 백만원")
        
        # 평가 요약
        st.subheader("평가 요약")
        summary_data = {
            "구분": ["회사명", "평가기준일", "매출액", "영업이익", "성장률", "할인율", "영업권 평가액"],
            "내용": [
                company_name if company_name else "미입력",
                evaluation_date.strftime("%Y-%m-%d"),
                f"{revenue:,.0f} 백만원",
                f"{operating_profit:,.0f} 백만원",
                f"{growth_rate:.1f}%",
                f"{adjusted_discount_rate:.1f}%",
                f"{goodwill_value:,.0f} 백만원"
            ]
        }
        st.table(pd.DataFrame(summary_data))
    
    except Exception as e:
        st.error(f"계산 중 오류가 발생했습니다: {str(e)}")
        st.warning("입력값을 확인하고 다시 시도해주세요.") 