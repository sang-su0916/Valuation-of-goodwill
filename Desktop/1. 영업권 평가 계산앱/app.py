import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import base64
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import math

# API 키 설정 (환경 변수에서 가져오거나 기본값 사용)
default_api_key = os.environ.get("GEMINI_API_KEY", "")

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
    
    # API 키 입력
    api_key = st.text_input("API 키 (전문가 모드)", value="", type="password")
    
    # API 키 유무에 따른 모드 표시
    if api_key:
        st.success("전문가 모드 활성화: 모든 기능 사용 가능")
    else:
        st.warning("기본 모드: 개인사업자 법인전환 탁상감정만 가능합니다. 전문가 모드를 사용하려면 API 키를 입력하세요.")
    
    # 평가 유형 선택 (API 키 유무에 따라 다르게 표시)
    if api_key:
        valuation_type = st.selectbox(
            "평가 유형",
            [
                "개인사업자 법인전환",
                "영업권 가치평가",
                "합병/인수 평가",
                "지식재산권 평가",
                "프랜차이즈 평가"
            ]
        )
    else:
        valuation_type = "개인사업자 법인전환"  # API 키가 없으면 기본값으로 고정
        st.info("다른 평가 유형을 사용하려면 API 키가 필요합니다.")
    
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
    
    # API 키가 있는 경우 추가 옵션 표시
    if api_key:
        st.subheader("추가 옵션")
        industry_factor = st.slider("산업 특성 계수", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
        risk_factor = st.slider("위험 계수", min_value=0.5, max_value=2.0, value=1.0, step=0.1)
    
    # 계산 버튼
    if st.button("평가 계산", type="primary"):
        st.session_state.calculate = True
    else:
        st.session_state.calculate = False

# PDF 생성 함수
def create_pdf_report(data):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # 제목
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "영업권 평가 보고서")
    
    # 기본 정보
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 100, "기본 정보")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 120, f"회사명: {data['company_name']}")
    c.drawString(50, height - 140, f"평가 기준일: {data['evaluation_date']}")
    c.drawString(50, height - 160, f"평가 유형: {data['valuation_type']}")
    
    # 재무 정보
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 200, "재무 정보")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 220, f"매출액: {data['revenue']:,.0f} 백만원")
    c.drawString(50, height - 240, f"영업이익: {data['operating_profit']:,.0f} 백만원")
    c.drawString(50, height - 260, f"성장률: {data['growth_rate']:.1f}%")
    c.drawString(50, height - 280, f"할인율: {data['discount_rate']:.1f}%")
    
    # 결과
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 320, "평가 결과")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 340, f"영업권 평가액: {data['goodwill_value']:,.0f} 백만원")
    
    # 평가 방법론
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 380, "평가 방법론")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 400, "현금흐름할인법(DCF)을 기반으로 한 영업권 가치평가")
    
    c.save()
    buffer.seek(0)
    return buffer

# 메인 화면
if 'calculate' in st.session_state and st.session_state.calculate:
    # 데이터 준비
    years = range(1, 6)
    
    # API 키 유무에 따른 계산 로직 차이
    if api_key:
        # 전문가 모드 계산
        industry_factor = st.session_state.get('industry_factor', 1.0)
        risk_factor = st.session_state.get('risk_factor', 1.0)
        
        # 더 정교한 성장 모델 적용
        revenues = [revenue * (1 + growth_rate/100 * math.exp(-0.1 * year) * industry_factor)**year for year in years]
        profit_margin = operating_profit/revenue * risk_factor
        profits = [rev * profit_margin for rev in revenues]
        
        # 전문가용 할인율 조정
        adjusted_discount_rate = discount_rate * risk_factor
    else:
        # 기본 모드 계산 (단순한 모델)
        revenues = [revenue * (1 + growth_rate/100)**year for year in years]
        profits = [rev * (operating_profit/revenue) for rev in revenues]
        adjusted_discount_rate = discount_rate
    
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
    present_values = [profit / ((1 + adjusted_discount_rate/100)**year) for year, profit in zip(years, profits)]
    goodwill_value = sum(present_values)
    
    # API 키가 있는 경우 보다 상세한 분석 제공
    if api_key:
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("현금흐름 할인 분석")
            df_dcf = pd.DataFrame({
                '연도': [f'{year}년차' for year in years],
                '영업이익': profits,
                '할인율': [f'{adjusted_discount_rate:.1f}%' for _ in years],
                '현재가치': present_values
            })
            st.dataframe(df_dcf)
        
        with col4:
            st.subheader("민감도 분석")
            # 성장률과 할인율 변화에 따른 영업권 가치 변화 계산
            growth_range = [growth_rate - 2, growth_rate, growth_rate + 2]
            discount_range = [adjusted_discount_rate - 2, adjusted_discount_rate, adjusted_discount_rate + 2]
            
            sensitivity_data = []
            for g in growth_range:
                if g < 0: continue  # 음수 성장률 제외
                row = []
                for d in discount_range:
                    if d <= 0: continue  # 0 이하 할인율 제외
                    rev = [revenue * (1 + g/100 * math.exp(-0.1 * year) * industry_factor)**year for year in years]
                    prof = [r * profit_margin for r in rev]
                    pv = [p / ((1 + d/100)**year) for year, p in zip(years, prof)]
                    row.append(sum(pv))
                sensitivity_data.append(row)
            
            # 히트맵으로 표시
            fig = go.Figure(data=go.Heatmap(
                z=sensitivity_data,
                x=[f'{d:.1f}%' for d in discount_range],
                y=[f'{g:.1f}%' for g in growth_range if g >= 0],
                colorscale='Viridis',
                hoverongaps=False))
            fig.update_layout(
                title='성장률/할인율 민감도 분석',
                xaxis_title='할인율',
                yaxis_title='성장률')
            st.plotly_chart(fig)
    
    st.metric("영업권 평가액", f"{goodwill_value:,.0f} 백만원")
    
    # 평가 요약
    st.subheader("평가 요약")
    summary_data = {
        "구분": ["회사명", "평가기준일", "평가유형", "매출액", "영업이익", "성장률", "할인율", "영업권 평가액"],
        "내용": [
            company_name,
            evaluation_date.strftime("%Y-%m-%d"),
            valuation_type,
            f"{revenue:,.0f} 백만원",
            f"{operating_profit:,.0f} 백만원",
            f"{growth_rate:.1f}%",
            f"{adjusted_discount_rate:.1f}%",
            f"{goodwill_value:,.0f} 백만원"
        ]
    }
    st.table(pd.DataFrame(summary_data))
    
    # API 키가 있는 경우에만 다운로드 버튼 표시
    if api_key:
        # PDF 보고서 생성
        report_data = {
            'company_name': company_name,
            'evaluation_date': evaluation_date.strftime("%Y-%m-%d"),
            'valuation_type': valuation_type,
            'revenue': revenue,
            'operating_profit': operating_profit,
            'growth_rate': growth_rate,
            'discount_rate': adjusted_discount_rate,
            'goodwill_value': goodwill_value
        }
        
        pdf_buffer = create_pdf_report(report_data)
        pdf_b64 = base64.b64encode(pdf_buffer.read()).decode()
        
        st.download_button(
            label="평가 보고서 다운로드 (PDF)",
            data=pdf_buffer,
            file_name=f"{company_name}_영업권평가보고서_{evaluation_date.strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            key='download-pdf'
        )
        
        st.success("전문가 모드: 상세 분석 및 보고서 다운로드가 활성화되었습니다.")
    else:
        st.info("전문가 모드를 사용하면 상세 분석과 보고서 다운로드가 가능합니다. API 키를 입력하세요.") 