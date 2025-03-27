import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="영업권 평가 시스템",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'
if 'company_data' not in st.session_state:
    st.session_state.company_data = {
        'name': '',
        'industry': '',
        'business_number': '',
        'financial_data': pd.DataFrame()
    }
if 'valuation_results' not in st.session_state:
    st.session_state.valuation_results = {}

def format_number(value):
    """숫자를 콤마가 포함된 문자열로 변환"""
    try:
        return f"{int(float(value)):,}"
    except (ValueError, TypeError):
        return ""

def parse_number(value):
    """콤마가 포함된 문자열을 숫자로 변환"""
    try:
        return float(value.replace(",", ""))
    except (ValueError, TypeError):
        return 0.0

# 사이드바 함수
def render_sidebar():
    with st.sidebar:
        st.image("https://via.placeholder.com/150x150.png?text=로고", width=150)
        st.title("영업권 평가 시스템")
        
        # 네비게이션 메뉴
        pages = {
            'home': '🏠 홈',
            'company_info': '📝 기업 정보 입력',
            'excess_earnings': '📊 초과이익법',
            'dcf': '💹 현금흐름할인법',
            'market_comparison': '🔍 시장가치비교법',
            'results': '📈 종합 결과',
            'report': '📑 보고서'
        }
        
        for page_id, page_name in pages.items():
            if st.button(page_name, key=f"nav_{page_id}"):
                st.session_state.current_page = page_id
                st.rerun()
        
        st.divider()
        # 연도 표시 제거
        # st.caption("© 2023 영업권 평가 시스템")

# 홈 페이지
def home_page():
    st.title("영업권 평가 시스템에 오신 것을 환영합니다")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ## 영업권이란?
        영업권은 기업의 순자산가치를 초과하는 가치로, 기업의 브랜드, 고객 관계, 기술력 등 무형의 가치를 포함합니다.
        기업 인수합병(M&A) 및 법인전환 과정에서 영업권의 가치 평가가 필수적입니다.
        
        ## 주요 평가 방법
        - **초과이익법**: 정상이익을 초과하는 이익을 계산하여 영업권 가치를 평가
        - **현금흐름할인법(DCF)**: 미래 예상 현금흐름을 현재가치화하여 평가
        - **시장가치비교법**: 유사 기업 비교를 통한 가치 산출
        """)
        
        # 추가 구현 예정 기능 홍보
        st.info("""
        ### 🚀 곧 출시될 기능
        - **AI 분석 보조**: 재무 데이터 분석 및 맞춤형 추천
        - **전문 PDF 보고서**: 전문가용 상세 보고서 자동 생성
        - **산업별 데이터베이스**: 더 정확한 비교를 위한 확장된 업종 데이터
        - **시계열 분석**: 영업권 가치 변동 추세 분석 및 예측
        """)
        
        # 상세 사용법 - 기본적으로 접혀있는 expander 사용
        with st.expander("📋 상세 사용 가이드", expanded=False):
            st.markdown("""
            ### 1. 기업 정보 입력
            - **기본 정보**: 회사명, 사업자등록번호, 산업군 등 기본 정보를 입력합니다.
            - **재무 데이터**: 최소 3년 이상의 재무제표 데이터를 입력합니다.
            - **CSV 업로드**: 기존 데이터를 CSV 형식으로 업로드할 수 있습니다.
            """)
            
            st.markdown("""
            ### 2. 초과이익법 평가
            - **정상 자본수익률**: 해당 업종의 평균 수익률을 설정합니다 (일반적으로 8-12%).
            - **초과이익 인정연수**: 초과이익이 지속될 것으로 예상되는 기간을 설정합니다 (보통 3-5년).
            - **할인율**: 미래 초과이익의 현재가치 계산에 사용됩니다 (10-15% 권장).
            - **고급 설정**: 조정 계수와 산업 프리미엄으로 기업 특성을 반영합니다.
            """)
            
            st.markdown("""
                ▪ 조정 계수: 일반 기업은 0.8-1.2, 식당업 등은 0.7-1.1 범위 내에서 설정
                ▪ 산업 프리미엄: 성장 산업은 높게, 쇠퇴 산업은 낮게 설정
            """)
            
            st.markdown("""
            ### 3. 현금흐름할인법(DCF) 평가
            - **기본 예측 설정**: 매출 성장률, 예측 기간, 영업이익률, 할인율 등 기본 설정
            - **고급 설정**: 연도별 맞춤 성장률, 자본 구조, 영구가치 계산 방법 등 설정
            - 미래 지향적 평가로, 성장 가능성이 큰 기업에 적합합니다.
            - 최소 2년의 재무제표로도 평가가 가능합니다.
            
            ### 4. 시장가치비교법 평가
            - **비교 지표 선택**: 매출액, 영업이익, 당기순이익, 총자산, EBITDA 등 지표 선택
            - **업종 평균 배수**: 선택된 지표에 적용할 업종 평균 배수 설정
            - **유사 기업 데이터**: 업종 내 유사 기업과의 비교 분석
            
            ### 5. 종합 결과 확인
            - 여러 방법의 평가 결과를 비교합니다.
            - 각 방법에 가중치를 적용하여 최종 영업권 가치를 산출합니다.
            - 차트와 그래프로 결과를 시각화합니다.
            
            ### 사용 팁
            - **업종별 접근**: 제조업은 현금흐름할인법, 소상공인은 초과이익법 선호
            - **데이터 품질**: 정확한 재무 데이터가 평가 결과의 품질을 좌우합니다
            - **결과 해석**: 단일 방법보다 여러 방법의 결과를 종합적으로 검토하세요
            - **법인 전환 시**: 세무사들이 주로 사용하는 초과이익법 결과를 중점적으로 검토하세요
            """)
        
        # 전문가 자문 안내
        st.warning("""
        ### ⚠️ 중요 안내사항
        이 앱은 영업권 평가를 위한 참고용 도구입니다. **실제 법적/세무적 목적의 영업권 평가는 반드시 세무사, 회계사, 또는 감정평가사의 전문적인 자문과 검토를 받으시기 바랍니다.**
        
        특히 다음의 경우 전문가 상담이 필수적입니다:
        - 법인 전환 및 사업 양도 시 과세 관련 평가
        - M&A 및 기업 인수 과정에서의 가치 평가
        - 금융기관 제출용 자산 평가
        - 법정 분쟁 및 소송 관련 감정 평가
        """)
        
        if st.button("시작하기", key="start_button"):
            st.session_state.current_page = 'company_info'
            st.rerun()
    
    with col2:
        st.image("https://via.placeholder.com/300x400.png?text=영업권+평가+예시", width=300)
        
        st.info("영업권 가치 평가는 기업의 현재와 미래 가치를 정확히 파악하는 데 중요합니다.")
        
        # 평가 방법 선택 가이드
        with st.expander("🔍 어떤 평가 방법이 적합할까요?", expanded=False):
            st.markdown("""
            ### 초과이익법 추천 대상
            - **개인사업자의 법인전환**
            - **소상공인/중소기업**
            - **세무적 목적의 평가**
            - **안정적인 수익 패턴을 가진 기업**
            
            ### 현금흐름할인법(DCF) 추천 대상
            - **성장 단계의 기업**
            - **미래 현금흐름 예측이 가능한 기업**
            - **투자 유치나 M&A 준비 기업**
            - **재무 구조 개선 중인 기업**
            
            ### 시장가치비교법 추천 대상
            - **유사 기업이 많은 일반적인 업종**
            - **상대 평가가 필요한 경우**
            - **빠른 참고 평가가 필요한 경우**
            - **시장 평균과의 비교가 중요한 경우**
            """)
        
        # 제품 버전 정보 삭제
        # st.caption("버전: 1.0.0 | 업데이트: 2024년 3월")

# 기업 정보 입력 페이지
def company_info_page():
    st.title("기업 정보 입력")
    
    with st.form("company_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input("회사명", value=st.session_state.company_data.get('name', ''))
            business_number = st.text_input("사업자등록번호", value=st.session_state.company_data.get('business_number', ''))
        
        with col2:
            industries = ["제조업", "서비스업", "도소매업", "IT/소프트웨어", "금융업", "건설업", "기타"]
            industry = st.selectbox("산업군", options=industries, index=0 if not st.session_state.company_data.get('industry') else industries.index(st.session_state.company_data.get('industry')))
        
        st.subheader("재무 데이터 입력")
        
        # 샘플 데이터 생성 또는 기존 데이터 불러오기
        if not isinstance(st.session_state.company_data.get('financial_data'), pd.DataFrame) or st.session_state.company_data.get('financial_data').empty:
            years = [datetime.now().year - i for i in range(1, 6)]
            sample_data = {
                '연도': years,
                '매출액': [0] * 5,
                '영업이익': [0] * 5,
                '당기순이익': [0] * 5,
                '총자산': [0] * 5,
                '총부채': [0] * 5,
                '자본': [0] * 5
            }
            financial_data = pd.DataFrame(sample_data)
        else:
            financial_data = st.session_state.company_data.get('financial_data')
        
        # 편집 가능한 데이터프레임 (단순화된 버전)
        edited_df = st.data_editor(financial_data, use_container_width=True)
        
        submit_button = st.form_submit_button("저장")
        
        if submit_button:
            # 데이터 유효성 검사
            if not company_name:
                st.warning("회사명을 입력해주세요.")
            else:
                # 데이터 저장
                st.session_state.company_data = {
                    'name': company_name,
                    'industry': industry,
                    'business_number': business_number,
                    'financial_data': edited_df
                }
                st.success("기업 정보가 저장되었습니다!")
    
    # 데이터 업로드/다운로드 기능
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("데이터 업로드")
        uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.dataframe(df.head())
                if st.button("이 데이터로 사용하기"):
                    st.session_state.company_data['financial_data'] = df
                    st.success("데이터가 성공적으로 로드되었습니다!")
                    st.rerun()
            except Exception as e:
                st.error(f"파일 로딩 중 오류 발생: {e}")
    
    with col2:
        st.subheader("데이터 다운로드")
        if not st.session_state.company_data.get('financial_data').empty:
            csv = st.session_state.company_data.get('financial_data').to_csv(index=False)
            st.download_button(
                label="CSV로 다운로드",
                data=csv,
                file_name=f"{st.session_state.company_data.get('name', 'company')}_financial_data.csv",
                mime='text/csv'
            )

# 초과이익법 페이지
def excess_earnings_page():
    st.title("초과이익법 평가")
    
    # 기업 데이터 확인
    if st.session_state.company_data.get('name') == '':
        st.warning("기업 정보가 입력되지 않았습니다. 먼저 기업 정보를 입력해주세요.")
        if st.button("기업 정보 입력으로 이동"):
            st.session_state.current_page = 'company_info'
            st.rerun()
        return
    
    st.subheader(f"{st.session_state.company_data.get('name')} - 초과이익법 평가")
    
    # 초과이익법 파라미터 설정
    with st.form("excess_earnings_params"):
        st.subheader("평가 매개변수 설정")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 정상 자본수익률 입력
            normal_roi_input = st.text_input("정상 자본수익률 (%)", value=format_number(normal_roi))
            if normal_roi_input:
                normal_roi = parse_number(normal_roi_input)
            excess_years_input = st.text_input("초과이익 인정연수", value=format_number(excess_years))
            if excess_years_input:
                excess_years = int(parse_number(excess_years_input))
            discount_rate = st.slider("할인율 (%)", min_value=5.0, max_value=30.0, value=12.0, step=0.5)
            weight_recent = st.checkbox("최근 연도에 가중치 부여", value=True)
        
        with col2:
            # 산업 프리미엄 입력
            industry_premium_input = st.text_input("산업 프리미엄 (%)", value=format_number(industry_premium))
            if industry_premium_input:
                industry_premium = parse_number(industry_premium_input)
            
            # 고급 설정
            with st.expander("고급 설정"):
                adjustment_factor = st.slider("조정 계수", min_value=0.5, max_value=1.5, value=1.0, step=0.1)
            
        calculate_button = st.form_submit_button("평가 계산")
        
        if calculate_button:
            try:
                # 데이터 가져오기
                df = st.session_state.company_data.get('financial_data')
                
                # 계산 로직 (간단한 예시)
                avg_earnings = df['당기순이익'].mean()
                total_assets = df['총자산'].iloc[0]  # 최신 연도 사용
                
                normal_profit = total_assets * (normal_roi / 100)
                excess_profit = avg_earnings - normal_profit
                
                if excess_profit <= 0:
                    st.error("초과이익이 계산되지 않습니다. 평균 이익이 정상 이익보다 낮습니다.")
                    return
                
                # 현재가치 계산
                present_value = 0
                for year in range(1, excess_years + 1):
                    discount_factor = 1 / ((1 + discount_rate/100) ** year)
                    present_value += excess_profit * discount_factor
                
                # 조정
                present_value = present_value * adjustment_factor * (1 + industry_premium/100)
                
                # 결과 저장
                st.session_state.valuation_results['excess_earnings'] = {
                    'method': '초과이익법',
                    'value': present_value,
                    'parameters': {
                        'normal_roi': normal_roi,
                        'excess_years': excess_years,
                        'discount_rate': discount_rate,
                        'adjustment_factor': adjustment_factor,
                        'industry_premium': industry_premium
                    },
                    'details': {
                        'avg_earnings': avg_earnings,
                        'total_assets': total_assets,
                        'normal_profit': normal_profit,
                        'excess_profit': excess_profit
                    }
                }
                
                st.success("초과이익법 평가가 완료되었습니다!")
                
            except Exception as e:
                st.error(f"계산 중 오류가 발생했습니다: {e}")
    
    # 계산 결과 표시 (이미 계산된 경우)
    if 'excess_earnings' in st.session_state.valuation_results:
        result = st.session_state.valuation_results['excess_earnings']
        
        st.divider()
        st.subheader("평가 결과")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("영업권 평가액", f"{result['value']:,.0f}원")
            
            st.subheader("주요 매개변수")
            params_df = pd.DataFrame({
                '매개변수': ['정상 자본수익률', '초과이익 인정연수', '할인율', '조정 계수', '산업 프리미엄'],
                '값': [
                    f"{result['parameters']['normal_roi']}%",
                    f"{result['parameters']['excess_years']}년",
                    f"{result['parameters']['discount_rate']}%",
                    f"{result['parameters']['adjustment_factor']}",
                    f"{result['parameters']['industry_premium']}%"
                ]
            })
            st.dataframe(params_df, hide_index=True)
        
        with col2:
            # 계산 과정 표시
            with st.expander("상세 계산 과정", expanded=True):
                st.markdown(f"""
                #### 1. 기초 데이터
                - 평균 당기순이익: {result['details']['avg_earnings']:,.0f}원
                - 총자산: {result['details']['total_assets']:,.0f}원
                
                #### 2. 정상이익 계산
                - 정상이익 = 총자산 × 정상수익률
                - 정상이익 = {result['details']['total_assets']:,.0f} × {result['parameters']['normal_roi']}% = {result['details']['normal_profit']:,.0f}원
                
                #### 3. 초과이익 계산
                - 초과이익 = 평균이익 - 정상이익
                - 초과이익 = {result['details']['avg_earnings']:,.0f} - {result['details']['normal_profit']:,.0f} = {result['details']['excess_profit']:,.0f}원
                
                #### 4. 현재가치 계산
                - {result['parameters']['excess_years']}년 동안 초과이익의 현재가치 합계
                - 할인율: {result['parameters']['discount_rate']}%
                
                #### 5. 조정
                - 조정 계수: {result['parameters']['adjustment_factor']}
                - 산업 프리미엄: {result['parameters']['industry_premium']}%
                
                #### 최종 영업권 가치
                - **{result['value']:,.0f}원**
                """)
            
            # 간단한 차트
            years = list(range(1, result['parameters']['excess_years'] + 1))
            values = []
            for year in years:
                discount_factor = 1 / ((1 + result['parameters']['discount_rate']/100) ** year)
                value = result['details']['excess_profit'] * discount_factor
                values.append(value)
            
            fig = px.bar(
                x=years,
                y=values,
                labels={'x': '연도', 'y': '현재가치'},
                title='연도별 초과이익의 현재가치'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # 결과 페이지로 이동 버튼
        if st.button("종합 결과 페이지로 이동"):
            st.session_state.current_page = 'results'
            st.rerun()

# 현금흐름할인법 페이지 (간소화된 버전)
def dcf_page():
    st.title("현금흐름할인법(DCF) 평가")
    
    # 기업 데이터 확인
    if st.session_state.company_data.get('name') == '':
        st.warning("기업 정보가 입력되지 않았습니다. 먼저 기업 정보를 입력해주세요.")
        if st.button("기업 정보 입력으로 이동"):
            st.session_state.current_page = 'company_info'
            st.rerun()
        return
    
    st.subheader(f"{st.session_state.company_data.get('name')} - 현금흐름할인법(DCF) 평가")
    
    # 초기 재무 데이터 가져오기
    financial_data = st.session_state.company_data.get('financial_data')
    
    # 마지막 연도 선택 (가장 최근 데이터)
    if not financial_data.empty:
        latest_year = financial_data['연도'].max()
        latest_data = financial_data[financial_data['연도'] == latest_year].iloc[0]
    else:
        st.warning("재무 데이터가 없습니다. 기업 정보 페이지에서 재무 데이터를 입력해주세요.")
        return
    
    # 탭 생성 (기본 설정 / 고급 설정)
    tab1, tab2 = st.tabs(["기본 예측 설정", "고급 설정"])
    
    with tab1:
        # 기본 DCF 파라미터 설정
        with st.form("dcf_basic_params"):
            st.subheader("기본 예측 설정")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 성장률 및 예측 기간 설정
                growth_rate = st.slider("연간 매출 성장률 (%)", min_value=-20.0, max_value=50.0, value=5.0, step=0.5)
                forecast_period = st.slider("예측 기간 (년)", min_value=3, max_value=10, value=5)
                
                # 영업이익률 설정
                operating_margin = st.slider("영업이익률 (%)", 
                                           min_value=0.0, 
                                           max_value=50.0, 
                                           value=float(latest_data['영업이익'] / latest_data['매출액'] * 100) if latest_data['매출액'] > 0 else 10.0,
                                           step=0.5)
            
            with col2:
                # 할인율 설정
                discount_rate = st.slider("할인율 (WACC, %)", min_value=5.0, max_value=30.0, value=12.0, step=0.5)
                
                # 영구 성장률 설정
                terminal_growth_rate = st.slider("영구 성장률 (%)", min_value=0.0, max_value=5.0, value=1.0, step=0.1,
                                              help="영구 성장률은 일반적으로 장기 GDP 성장률과 인플레이션을 고려하여 1-3% 사이로 설정합니다.")
                
                # 법인세율 설정
                tax_rate = st.slider("법인세율 (%)", min_value=10.0, max_value=30.0, value=22.0, step=0.5)
            
            calculate_basic_button = st.form_submit_button("기본 DCF 계산")
            
            if calculate_basic_button:
                # DCF 계산 로직
                try:
                    # 기준 데이터 설정
                    base_revenue = latest_data['매출액']
                    base_operating_income = latest_data['영업이익']
                    
                    # 미래 현금흐름 예측 결과를 저장할 DataFrame 생성
                    forecast_years = [latest_year + i for i in range(1, forecast_period + 1)]
                    forecast_df = pd.DataFrame(index=range(forecast_period), columns=[
                        '연도', '매출액', '영업이익', '세전이익', '세금', '세후이익', 
                        '감가상각비', '자본적지출', '운전자본증감', '잉여현금흐름', '할인계수', '현재가치'
                    ])
                    
                    # 예측 데이터 계산
                    for i in range(forecast_period):
                        forecast_df.loc[i, '연도'] = forecast_years[i]
                        
                        # 매출액 예측
                        if i == 0:
                            forecast_df.loc[i, '매출액'] = base_revenue * (1 + growth_rate / 100)
                        else:
                            forecast_df.loc[i, '매출액'] = forecast_df.loc[i-1, '매출액'] * (1 + growth_rate / 100)
                        
                        # 영업이익 예측
                        forecast_df.loc[i, '영업이익'] = forecast_df.loc[i, '매출액'] * operating_margin / 100
                        
                        # 세전이익 (영업이익과 동일하게 가정)
                        forecast_df.loc[i, '세전이익'] = forecast_df.loc[i, '영업이익']
                        
                        # 세금 계산
                        forecast_df.loc[i, '세금'] = forecast_df.loc[i, '세전이익'] * tax_rate / 100
                        
                        # 세후이익 계산
                        forecast_df.loc[i, '세후이익'] = forecast_df.loc[i, '세전이익'] - forecast_df.loc[i, '세금']
                        
                        # 감가상각비 (매출액의 3%로 가정, 실제로는 더 정교한 모델 필요)
                        forecast_df.loc[i, '감가상각비'] = forecast_df.loc[i, '매출액'] * 0.03
                        
                        # 자본적지출 (매출액의 5%로 가정)
                        forecast_df.loc[i, '자본적지출'] = forecast_df.loc[i, '매출액'] * 0.05
                        
                        # 운전자본증감 (매출액 증가의 10%로 가정)
                        if i == 0:
                            revenue_increase = forecast_df.loc[i, '매출액'] - base_revenue
                        else:
                            revenue_increase = forecast_df.loc[i, '매출액'] - forecast_df.loc[i-1, '매출액']
                        
                        forecast_df.loc[i, '운전자본증감'] = revenue_increase * 0.1 if revenue_increase > 0 else 0
                        
                        # 잉여현금흐름 계산
                        forecast_df.loc[i, '잉여현금흐름'] = (
                            forecast_df.loc[i, '세후이익'] + 
                            forecast_df.loc[i, '감가상각비'] - 
                            forecast_df.loc[i, '자본적지출'] - 
                            forecast_df.loc[i, '운전자본증감']
                        )
                        
                        # 할인계수 계산
                        forecast_df.loc[i, '할인계수'] = 1 / ((1 + discount_rate / 100) ** (i + 1))
                        
                        # 현재가치 계산
                        forecast_df.loc[i, '현재가치'] = forecast_df.loc[i, '잉여현금흐름'] * forecast_df.loc[i, '할인계수']
                    
                    # 포맷팅을 위해 금액 컬럼을 정수로 변환
                    numeric_columns = [
                        '매출액', '영업이익', '세전이익', '세금', '세후이익', 
                        '감가상각비', '자본적지출', '운전자본증감', '잉여현금흐름', '현재가치'
                    ]
                    for col in numeric_columns:
                        forecast_df[col] = forecast_df[col].astype(int)
                    
                    # 단계별 현재가치의 합
                    total_present_value = forecast_df['현재가치'].sum()
                    
                    # 영구가치(Terminal Value) 계산
                    last_fcf = forecast_df.loc[forecast_period-1, '잉여현금흐름']
                    terminal_value = last_fcf * (1 + terminal_growth_rate / 100) / (discount_rate / 100 - terminal_growth_rate / 100)
                    terminal_value_present = terminal_value * forecast_df.loc[forecast_period-1, '할인계수']
                    
                    # 기업가치 계산
                    firm_value = total_present_value + terminal_value_present
                    
                    # 결과 표시
                    st.success("DCF 평가가 완료되었습니다!")
                    
                    # 예측 데이터 표시
                    st.subheader("미래 현금흐름 예측")
                    st.dataframe(forecast_df, hide_index=True, use_container_width=True)
                    
                    # 결과 요약 표시
                    st.subheader("DCF 평가 결과")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("예측 기간 현금흐름 합계", f"{total_present_value:,.0f}원")
                    with col2:
                        st.metric("잔존가치 현재가치", f"{terminal_value_present:,.0f}원")
                    with col3:
                        st.metric("총 기업가치", f"{firm_value:,.0f}원")
                    
                    # 영업권 가치 추정 (간소화: 기업가치 - 순자산가치)
                    # 실제로는 더 정교한 계산이 필요할 수 있음
                    net_asset_value = latest_data['총자산'] - latest_data['총부채'] if '총자산' in latest_data and '총부채' in latest_data else firm_value * 0.6
                    goodwill_value = firm_value - net_asset_value
                    
                    # 영업권 가치 표시
                    st.metric("추정 영업권 가치", f"{goodwill_value:,.0f}원")
                    
                    # 결과 저장
                    st.session_state.valuation_results['dcf'] = {
                        'method': '현금흐름할인법(DCF)',
                        'value': goodwill_value,
                        'parameters': {
                            'growth_rate': growth_rate,
                            'forecast_period': forecast_period,
                            'operating_margin': operating_margin,
                            'discount_rate': discount_rate,
                            'terminal_growth_rate': terminal_growth_rate,
                            'tax_rate': tax_rate
                        },
                        'details': {
                            'firm_value': firm_value,
                            'net_asset_value': net_asset_value,
                            'total_present_value': total_present_value,
                            'terminal_value': terminal_value,
                            'terminal_value_present': terminal_value_present
                        }
                    }
                    
                    # 차트 표시
                    st.subheader("현금흐름 분석")
                    
                    # 현금흐름 추이 차트
                    fig_fcf = px.line(
                        forecast_df, 
                        x='연도', 
                        y=['잉여현금흐름', '현재가치'], 
                        title='예측 기간 현금흐름 추이',
                        labels={'value': '금액', 'variable': '구분'}
                    )
                    st.plotly_chart(fig_fcf, use_container_width=True)
                    
                    # 기업가치 구성 파이 차트
                    fig_value = px.pie(
                        names=['예측기간 현재가치', '잔존가치 현재가치'],
                        values=[total_present_value, terminal_value_present],
                        title='기업가치 구성'
                    )
                    st.plotly_chart(fig_value, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"DCF 계산 중 오류가 발생했습니다: {e}")
    
    with tab2:
        # 고급 DCF 설정
        with st.form("dcf_advanced_params"):
            st.subheader("고급 DCF 설정")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # 연도별 맞춤 예측 설정
                st.markdown("#### 연도별 맞춤 성장률 설정")
                custom_growth = {}
                
                for i in range(1, 6):
                    year = latest_year + i
                    custom_growth[year] = st.slider(
                        f"{year}년 매출 성장률 (%)", 
                        min_value=-20.0, 
                        max_value=50.0, 
                        value=5.0 if i <= 2 else 3.0,  # 초기엔 높은 성장률, 이후 안정화
                        step=0.5
                    )
            
            with col2:
                # 자본 구조 설정
                st.markdown("#### 자본 구조 및 비용")
                debt_ratio = st.slider("부채 비율 (%)", min_value=0.0, max_value=80.0, value=30.0, step=1.0)
                cost_of_debt = st.slider("부채 비용 (%)", min_value=1.0, max_value=15.0, value=5.0, step=0.5)
                cost_of_equity = st.slider("자기자본 비용 (%)", min_value=5.0, max_value=30.0, value=15.0, step=0.5)
                
                # WACC 자동 계산
                equity_ratio = 100 - debt_ratio
                wacc = (debt_ratio / 100 * cost_of_debt * (1 - 22/100)) + (equity_ratio / 100 * cost_of_equity)
                st.metric("계산된 WACC (%)", f"{wacc:.2f}%")
            
            # 고급 영구가치 설정
            st.markdown("#### 영구가치 설정")
            terminal_value_method = st.selectbox("영구가치 계산 방법", 
                                            options=["영구성장모델(Gordon Growth)", "Exit Multiple"])
            
            if terminal_value_method == "Exit Multiple":
                exit_multiple = st.slider("Exit Multiple (EBITDA 배수)", min_value=3.0, max_value=15.0, value=6.0, step=0.5)
            
            calculate_advanced_button = st.form_submit_button("고급 DCF 계산")
            
            if calculate_advanced_button:
                # 고급 DCF 계산 로직
                try:
                    # 기준 데이터 설정
                    base_revenue = latest_data['매출액']
                    base_operating_income = latest_data['영업이익']
                    
                    # 미래 현금흐름 예측 결과를 저장할 DataFrame 생성
                    forecast_period = 5  # 고정 5년
                    forecast_years = [latest_year + i for i in range(1, forecast_period + 1)]
                    forecast_df = pd.DataFrame(index=range(forecast_period), columns=[
                        '연도', '매출액', '영업이익', '세전이익', '세금', '세후이익', 
                        '감가상각비', '자본적지출', '운전자본증감', '잉여현금흐름', '할인계수', '현재가치'
                    ])
                    
                    # 예측 데이터 계산
                    for i in range(forecast_period):
                        year = forecast_years[i]
                        forecast_df.loc[i, '연도'] = year
                        
                        # 매출액 예측 (맞춤 성장률 적용)
                        if i == 0:
                            forecast_df.loc[i, '매출액'] = base_revenue * (1 + custom_growth[year] / 100)
                        else:
                            prev_year = forecast_years[i-1]
                            forecast_df.loc[i, '매출액'] = forecast_df.loc[i-1, '매출액'] * (1 + custom_growth[year] / 100)
                        
                        # 영업이익 예측 (영업이익률은 간소화)
                        forecast_df.loc[i, '영업이익'] = forecast_df.loc[i, '매출액'] * operating_margin / 100
                        
                        # 세전이익 (영업이익과 동일하게 가정)
                        forecast_df.loc[i, '세전이익'] = forecast_df.loc[i, '영업이익']
                        
                        # 세금 계산
                        forecast_df.loc[i, '세금'] = forecast_df.loc[i, '세전이익'] * tax_rate / 100
                        
                        # 세후이익 계산
                        forecast_df.loc[i, '세후이익'] = forecast_df.loc[i, '세전이익'] - forecast_df.loc[i, '세금']
                        
                        # 감가상각비 (매출액의 3%로 가정)
                        forecast_df.loc[i, '감가상각비'] = forecast_df.loc[i, '매출액'] * 0.03
                        
                        # 자본적지출 (매출액의 5%로 가정)
                        forecast_df.loc[i, '자본적지출'] = forecast_df.loc[i, '매출액'] * 0.05
                        
                        # 운전자본증감 (매출액 증가의 10%로 가정)
                        if i == 0:
                            revenue_increase = forecast_df.loc[i, '매출액'] - base_revenue
                        else:
                            revenue_increase = forecast_df.loc[i, '매출액'] - forecast_df.loc[i-1, '매출액']
                        
                        forecast_df.loc[i, '운전자본증감'] = revenue_increase * 0.1 if revenue_increase > 0 else 0
                        
                        # 잉여현금흐름 계산
                        forecast_df.loc[i, '잉여현금흐름'] = (
                            forecast_df.loc[i, '세후이익'] + 
                            forecast_df.loc[i, '감가상각비'] - 
                            forecast_df.loc[i, '자본적지출'] - 
                            forecast_df.loc[i, '운전자본증감']
                        )
                        
                        # 할인계수 계산 (WACC 사용)
                        forecast_df.loc[i, '할인계수'] = 1 / ((1 + wacc / 100) ** (i + 1))
                        
                        # 현재가치 계산
                        forecast_df.loc[i, '현재가치'] = forecast_df.loc[i, '잉여현금흐름'] * forecast_df.loc[i, '할인계수']
                    
                    # 포맷팅을 위해 금액 컬럼을 정수로 변환
                    numeric_columns = [
                        '매출액', '영업이익', '세전이익', '세금', '세후이익', 
                        '감가상각비', '자본적지출', '운전자본증감', '잉여현금흐름', '현재가치'
                    ]
                    for col in numeric_columns:
                        forecast_df[col] = forecast_df[col].astype(int)
                    
                    # 단계별 현재가치의 합
                    total_present_value = forecast_df['현재가치'].sum()
                    
                    # 영구가치(Terminal Value) 계산
                    last_fcf = forecast_df.loc[forecast_period-1, '잉여현금흐름']
                    
                    if terminal_value_method == "영구성장모델(Gordon Growth)":
                        terminal_value = last_fcf * (1 + terminal_growth_rate / 100) / (wacc / 100 - terminal_growth_rate / 100)
                    else:  # Exit Multiple
                        last_ebitda = forecast_df.loc[forecast_period-1, '영업이익'] + forecast_df.loc[forecast_period-1, '감가상각비']
                        terminal_value = last_ebitda * exit_multiple
                    
                    terminal_value_present = terminal_value * forecast_df.loc[forecast_period-1, '할인계수']
                    
                    # 기업가치 계산
                    firm_value = total_present_value + terminal_value_present
                    
                    # 결과 표시
                    st.success("고급 DCF 평가가 완료되었습니다!")
                    
                    # 예측 데이터 표시
                    st.subheader("미래 현금흐름 예측")
                    st.dataframe(forecast_df, hide_index=True, use_container_width=True)
                    
                    # 결과 요약 표시
                    st.subheader("DCF 평가 결과")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("예측 기간 현금흐름 합계", f"{total_present_value:,.0f}원")
                    with col2:
                        st.metric("잔존가치 현재가치", f"{terminal_value_present:,.0f}원")
                    with col3:
                        st.metric("총 기업가치", f"{firm_value:,.0f}원")
                    
                    # 영업권 가치 추정 (간소화: 기업가치 - 순자산가치)
                    net_asset_value = latest_data['총자산'] - latest_data['총부채'] if '총자산' in latest_data and '총부채' in latest_data else firm_value * 0.6
                    goodwill_value = firm_value - net_asset_value
                    
                    # 영업권 가치 표시
                    st.metric("추정 영업권 가치", f"{goodwill_value:,.0f}원")
                    
                    # 결과 저장
                    st.session_state.valuation_results['dcf'] = {
                        'method': '현금흐름할인법(DCF)',
                        'value': goodwill_value,
                        'parameters': {
                            'custom_growth': custom_growth,
                            'operating_margin': operating_margin,
                            'wacc': wacc,
                            'terminal_growth_rate': terminal_growth_rate,
                            'terminal_value_method': terminal_value_method
                        },
                        'details': {
                            'firm_value': firm_value,
                            'net_asset_value': net_asset_value,
                            'total_present_value': total_present_value,
                            'terminal_value': terminal_value,
                            'terminal_value_present': terminal_value_present
                        }
                    }
                    
                    # 차트 표시
                    st.subheader("현금흐름 분석")
                    
                    # 현금흐름 추이 차트
                    fig_fcf = px.line(
                        forecast_df, 
                        x='연도', 
                        y=['잉여현금흐름', '현재가치'], 
                        title='예측 기간 현금흐름 추이',
                        labels={'value': '금액', 'variable': '구분'}
                    )
                    st.plotly_chart(fig_fcf, use_container_width=True)
                    
                    # 기업가치 구성 파이 차트
                    fig_value = px.pie(
                        names=['예측기간 현재가치', '잔존가치 현재가치'],
                        values=[total_present_value, terminal_value_present],
                        title='기업가치 구성'
                    )
                    st.plotly_chart(fig_value, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"고급 DCF 계산 중 오류가 발생했습니다: {e}")
    
    # 결과가 계산되었다면 종합 결과 페이지로 이동 버튼 표시
    if 'dcf' in st.session_state.valuation_results:
        if st.button("종합 결과 페이지로 이동"):
            st.session_state.current_page = 'results'
            st.rerun()

# 시장가치비교법 페이지 (간소화된 버전)
def market_comparison_page():
    st.title("시장가치비교법 평가")
    
    # 기업 데이터 확인
    if st.session_state.company_data.get('name') == '':
        st.warning("기업 정보가 입력되지 않았습니다. 먼저 기업 정보를 입력해주세요.")
        if st.button("기업 정보 입력으로 이동"):
            st.session_state.current_page = 'company_info'
            st.rerun()
        return
    
    st.subheader(f"{st.session_state.company_data.get('name')} - 시장가치비교법 평가")
    
    # 초기 재무 데이터 가져오기
    financial_data = st.session_state.company_data.get('financial_data')
    
    # 마지막 연도 선택 (가장 최근 데이터)
    if not financial_data.empty:
        latest_year = financial_data['연도'].max()
        latest_data = financial_data[financial_data['연도'] == latest_year].iloc[0]
    else:
        st.warning("재무 데이터가 없습니다. 기업 정보 페이지에서 재무 데이터를 입력해주세요.")
        return
    
    # 업종 정보 확인
    industry = st.session_state.company_data.get('industry', '일반')
    
    # 시장가치비교법 파라미터 설정
    with st.form("market_comparison_params"):
        st.subheader("평가 매개변수 설정")
        
        # 기업의 재무 지표 선택
        metrics_options = ['매출액', '영업이익', '당기순이익', '총자산', 'EBITDA']
        
        col1, col2 = st.columns(2)
        
        with col1:
            # 사용할 재무 지표 선택
            selected_metric = st.selectbox("비교 지표 선택", options=metrics_options)
            
            # 선택된 지표의 값 표시
            if selected_metric in latest_data:
                metric_value = latest_data[selected_metric]
                st.info(f"선택한 지표의 최근 연도({latest_year}) 값: {metric_value:,.0f}원")
            else:
                # EBITDA 계산 (영업이익 + 감가상각비)
                if selected_metric == 'EBITDA':
                    # 감가상각비가 없는 경우 영업이익의 10%로 가정
                    depreciation = latest_data.get('감가상각비', latest_data['영업이익'] * 0.1 if '영업이익' in latest_data else 0)
                    metric_value = latest_data['영업이익'] + depreciation if '영업이익' in latest_data else 0
                    st.info(f"계산된 EBITDA 값({latest_year}): {metric_value:,.0f}원")
                else:
                    st.warning(f"선택한 지표 '{selected_metric}'의 데이터가 없습니다.")
                    metric_value = 0
        
        with col2:
            # 업종별 평균 배수 (실제로는 DB나 API에서 가져와야 함)
            # 여기서는 간단한 예시 데이터 사용
            industry_multiples = {
                '제조업': {
                    '매출액': 0.8,
                    '영업이익': 6.5,
                    '당기순이익': 10.0,
                    '총자산': 1.2,
                    'EBITDA': 5.5
                },
                '서비스업': {
                    '매출액': 1.2,
                    '영업이익': 7.0,
                    '당기순이익': 12.0,
                    '총자산': 1.5,
                    'EBITDA': 6.0
                },
                'IT/소프트웨어': {
                    '매출액': 2.5,
                    '영업이익': 12.0,
                    '당기순이익': 18.0,
                    '총자산': 2.2,
                    'EBITDA': 10.0
                },
                '도소매업': {
                    '매출액': 0.7,
                    '영업이익': 5.5,
                    '당기순이익': 9.0,
                    '총자산': 1.0,
                    'EBITDA': 5.0
                },
                '금융업': {
                    '매출액': 1.5,
                    '영업이익': 8.0,
                    '당기순이익': 12.0,
                    '총자산': 0.8,
                    'EBITDA': 7.0
                },
                '건설업': {
                    '매출액': 0.6,
                    '영업이익': 5.0,
                    '당기순이익': 8.0,
                    '총자산': 0.9,
                    'EBITDA': 4.5
                },
                '기타': {
                    '매출액': 1.0,
                    '영업이익': 6.0,
                    '당기순이익': 10.0,
                    '총자산': 1.2,
                    'EBITDA': 5.5
                }
            }
            
            # 업종이 업종별 배수 데이터에 없으면 '기타' 사용
            if industry not in industry_multiples:
                industry = '기타'
                
            # 선택된 지표의 업종 평균 배수 가져오기
            default_multiple = industry_multiples[industry][selected_metric]
            
            # 사용자 정의 배수 입력 허용
            multiple_input = st.text_input("배수", value=format_number(multiple))
            if multiple_input:
                multiple = parse_number(multiple_input)
            
            # 조정 계수 설정
            adjustment_factor = st.slider(
                "조정 계수", 
                min_value=0.5, 
                max_value=1.5, 
                value=1.0, 
                step=0.05,
                help="기업의 특성을 고려한 추가 조정 요소입니다. 1보다 작으면 가치를 낮추고, 1보다 크면 가치를 높입니다."
            )
        
        # 유사 기업 데이터
        with st.expander("유사 기업 데이터"):
            st.markdown("#### 업종 내 유사 기업 비교")
            
            # 가상의 유사 기업 데이터 (실제로는 DB에서 가져와야 함)
            similar_companies = {
                '제조업': [
                    {'name': 'A제조', 'multiple': 5.8, 'revenue': 250000000000, 'profit': 15000000000},
                    {'name': 'B산업', 'multiple': 6.2, 'revenue': 180000000000, 'profit': 10000000000},
                    {'name': 'C기계', 'multiple': 7.1, 'revenue': 350000000000, 'profit': 22000000000}
                ],
                '서비스업': [
                    {'name': 'D서비스', 'multiple': 6.5, 'revenue': 120000000000, 'profit': 9000000000},
                    {'name': 'E컨설팅', 'multiple': 7.5, 'revenue': 80000000000, 'profit': 7500000000},
                    {'name': 'F솔루션', 'multiple': 7.0, 'revenue': 150000000000, 'profit': 12000000000}
                ],
                'IT/소프트웨어': [
                    {'name': 'G소프트', 'multiple': 11.5, 'revenue': 90000000000, 'profit': 12000000000},
                    {'name': 'H테크', 'multiple': 12.8, 'revenue': 120000000000, 'profit': 18000000000},
                    {'name': 'I솔루션', 'multiple': 11.7, 'revenue': 75000000000, 'profit': 9000000000}
                ],
                '도소매업': [
                    {'name': 'J유통', 'multiple': 5.2, 'revenue': 500000000000, 'profit': 12000000000},
                    {'name': 'K마트', 'multiple': 5.7, 'revenue': 450000000000, 'profit': 10000000000},
                    {'name': 'L상사', 'multiple': 5.6, 'revenue': 350000000000, 'profit': 8000000000}
                ],
                '금융업': [
                    {'name': 'M금융', 'multiple': 7.8, 'revenue': 220000000000, 'profit': 35000000000},
                    {'name': 'N캐피탈', 'multiple': 8.2, 'revenue': 180000000000, 'profit': 30000000000},
                    {'name': 'O파이낸스', 'multiple': 8.0, 'revenue': 200000000000, 'profit': 32000000000}
                ],
                '건설업': [
                    {'name': 'P건설', 'multiple': 4.8, 'revenue': 700000000000, 'profit': 21000000000},
                    {'name': 'Q엔지니어링', 'multiple': 5.2, 'revenue': 500000000000, 'profit': 18000000000},
                    {'name': 'R개발', 'multiple': 5.0, 'revenue': 600000000000, 'profit': 20000000000}
                ],
                '기타': [
                    {'name': '기업 X', 'multiple': 5.8, 'revenue': 150000000000, 'profit': 9000000000},
                    {'name': '기업 Y', 'multiple': 6.2, 'revenue': 180000000000, 'profit': 11000000000},
                    {'name': '기업 Z', 'multiple': 6.0, 'revenue': 160000000000, 'profit': 10000000000}
                ]
            }
            
            # 유사 기업이 없는 경우 기타 사용
            if industry not in similar_companies:
                industry_for_similar = '기타'
            else:
                industry_for_similar = industry
                
            # 유사 기업 테이블 표시
            similar_df = pd.DataFrame(similar_companies[industry_for_similar])
            similar_df.columns = ['기업명', f'{selected_metric} 배수', '매출액', '영업이익']
            # 금액 포맷팅
            similar_df['매출액'] = similar_df['매출액'].apply(lambda x: f"{x:,.0f}원")
            similar_df['영업이익'] = similar_df['영업이익'].apply(lambda x: f"{x:,.0f}원")
            
            st.dataframe(similar_df, hide_index=True)
            
            st.info(f"업종 내 유사 기업들의 평균 {selected_metric} 배수는 {similar_df[f'{selected_metric} 배수'].mean():.2f}입니다.")
        
        calculate_button = st.form_submit_button("평가 계산")
        
        if calculate_button:
            try:
                # 시장가치비교법 계산
                market_value = metric_value * multiple
                
                # 조정 계수 적용
                adjusted_market_value = market_value * adjustment_factor
                
                # 영업권 가치 추정 (간소화: 시장가치 - 순자산가치)
                net_asset_value = latest_data['총자산'] - latest_data['총부채'] if '총자산' in latest_data and '총부채' in latest_data else adjusted_market_value * 0.6
                goodwill_value = adjusted_market_value - net_asset_value
                
                # 결과 표시
                st.success("시장가치비교법 평가가 완료되었습니다!")
                
                # 결과 요약 표시
                st.subheader("평가 결과")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(f"{selected_metric} 기준 시장가치", f"{market_value:,.0f}원")
                
                with col2:
                    st.metric("조정된 시장가치", f"{adjusted_market_value:,.0f}원")
                
                with col3:
                    st.metric("추정 영업권 가치", f"{goodwill_value:,.0f}원")
                
                # 계산 과정 표시
                st.subheader("계산 과정")
                calc_df = pd.DataFrame({
                    '구분': [f"{selected_metric} 값", f"{selected_metric} 배수", "시장가치", "조정 계수", 
                           "조정된 시장가치", "순자산가치", "영업권 가치"],
                    '값': [f"{metric_value:,.0f}원", f"{multiple:.2f}", f"{market_value:,.0f}원", 
                          f"{adjustment_factor:.2f}", f"{adjusted_market_value:,.0f}원", 
                          f"{net_asset_value:,.0f}원", f"{goodwill_value:,.0f}원"]
                })
                
                st.dataframe(calc_df, hide_index=True, use_container_width=True)
                
                # 업종 내 위치 차트
                st.subheader("업종 내 위치")
                
                # 비교 차트 데이터 준비
                comparison_data = []
                
                # 유사 기업 데이터 추가
                for company in similar_companies[industry_for_similar]:
                    comparison_data.append({
                        '기업명': company['name'],
                        f'{selected_metric} 배수': company['multiple']
                    })
                
                # 현재 기업 데이터 추가
                comparison_data.append({
                    '기업명': st.session_state.company_data.get('name'),
                    f'{selected_metric} 배수': multiple
                })
                
                # 데이터프레임 생성
                comparison_df = pd.DataFrame(comparison_data)
                
                # 막대 차트로 표시
                fig = px.bar(
                    comparison_df, 
                    x='기업명', 
                    y=f'{selected_metric} 배수',
                    title=f'업종 내 {selected_metric} 배수 비교',
                    color='기업명',
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    text=f'{selected_metric} 배수'
                )
                
                fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
                fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 결과 저장
                st.session_state.valuation_results['market_comparison'] = {
                    'method': '시장가치비교법',
                    'value': goodwill_value,
                    'parameters': {
                        'selected_metric': selected_metric,
                        'metric_value': metric_value,
                        'multiple': multiple,
                        'adjustment_factor': adjustment_factor
                    },
                    'details': {
                        'market_value': market_value,
                        'adjusted_market_value': adjusted_market_value,
                        'net_asset_value': net_asset_value,
                        'industry': industry
                    }
                }
                
            except Exception as e:
                st.error(f"계산 중 오류가 발생했습니다: {e}")
    
    # 결과가 계산되었다면 종합 결과 페이지로 이동 버튼 표시
    if 'market_comparison' in st.session_state.valuation_results:
        if st.button("종합 결과 페이지로 이동"):
            st.session_state.current_page = 'results'
            st.rerun()

# 종합 결과 페이지
def results_page():
    st.title("종합 평가 결과")
    
    # 결과가 없는 경우
    if not st.session_state.valuation_results:
        st.warning("아직 평가된 결과가 없습니다. 먼저 평가 방법을 선택하여 계산해주세요.")
        return
    
    # 회사 정보 표시
    st.subheader(f"{st.session_state.company_data.get('name')} 영업권 평가 결과")
    st.caption(f"산업: {st.session_state.company_data.get('industry')} | 평가일: {datetime.now().strftime('%Y-%m-%d')}")
    
    # 전문가 자문 안내
    st.warning("""
    ### ⚠️ 주의사항
    본 평가 결과는 참고용이며, 실제 의사결정에는 세무사, 회계사, 감정평가사 등 전문가의 자문을 받으시기 바랍니다.
    특히 법인 전환, M&A, 세무신고 등의 목적으로 사용할 경우 반드시 전문가의 검토가 필요합니다.
    """)
    
    # 결과 요약
    methods = list(st.session_state.valuation_results.keys())
    values = [st.session_state.valuation_results[method]['value'] for method in methods]
    methods_names = [st.session_state.valuation_results[method]['method'] for method in methods]
    
    # 차트로 결과 표시
    fig = px.bar(
        x=methods_names,
        y=values,
        labels={'x': '평가 방법', 'y': '영업권 가치'},
        title='평가 방법별 영업권 가치 비교'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 결과 테이블
    results_df = pd.DataFrame({
        '평가 방법': methods_names,
        '영업권 가치(원)': [f"{value:,.0f}" for value in values]
    })
    st.dataframe(results_df, hide_index=True, use_container_width=True)
    
    # 가중평균 계산 (방법이 2개 이상인 경우)
    if len(methods) > 1:
        st.subheader("가중평균 영업권 가치")
        
        col1, col2 = st.columns(2)
        
        with col1:
            weights = {}
            for method in methods:
                weights[method] = st.slider(
                    f"{st.session_state.valuation_results[method]['method']} 가중치",
                    min_value=0.0,
                    max_value=1.0,
                    value=1.0/len(methods),
                    step=0.05,
                    key=f"weight_{method}"
                )
            
            # 가중치 정규화
            total_weight = sum(weights.values())
            if total_weight > 0:
                for method in weights:
                    weights[method] = weights[method] / total_weight
            
            # 가중평균 계산
            weighted_value = sum(st.session_state.valuation_results[method]['value'] * weights[method] for method in methods)
            
            st.metric("최종 영업권 가치", f"{weighted_value:,.0f}원")
        
        with col2:
            # 가중치 파이 차트
            fig = px.pie(
                names=methods_names,
                values=list(weights.values()),
                title='평가 방법 가중치'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # 보고서 페이지로 이동
    if st.button("보고서 생성하기"):
        st.session_state.current_page = 'report'
        st.rerun()

# 보고서 페이지 (간소화된 버전)
def report_page():
    st.title("평가 보고서")
    
    if not st.session_state.valuation_results:
        st.warning("아직 평가된 결과가 없습니다. 먼저 평가 방법을 선택하여 계산해주세요.")
        return
    
    st.info("PDF 보고서 생성 기능은 Phase 3에서 구현될 예정입니다.")
    
    # 전문가 검토 안내
    st.warning("""
    ### ⚠️ 전문가 검토 필요
    이 보고서는 자동 생성된 참고용 자료입니다. 실제 법적 효력이 필요한 경우나 중요한 의사결정에 활용하기 전에
    반드시 세무사, 회계사, 또는 감정평가사의 전문적인 검토를 받으시기 바랍니다.
    """)
    
    # 간단한 미리보기
    st.subheader("보고서 미리보기")
    
    # 회사 정보
    st.markdown(f"""
    ## 영업권 가치 평가 보고서
    
    **회사명**: {st.session_state.company_data.get('name')}  
    **산업**: {st.session_state.company_data.get('industry')}  
    **사업자등록번호**: {st.session_state.company_data.get('business_number')}  
    **평가일**: {datetime.now().strftime('%Y-%m-%d')}
    
    ### 평가 결과 요약
    """)
    
    # 결과 테이블
    methods = list(st.session_state.valuation_results.keys())
    values = [st.session_state.valuation_results[method]['value'] for method in methods]
    methods_names = [st.session_state.valuation_results[method]['method'] for method in methods]
    
    results_df = pd.DataFrame({
        '평가 방법': methods_names,
        '영업권 가치(원)': [f"{value:,.0f}" for value in values]
    })
    st.dataframe(results_df, hide_index=True, use_container_width=True)
    
    # 차트
    fig = px.bar(
        x=methods_names,
        y=values,
        labels={'x': '평가 방법', 'y': '영업권 가치'},
        title='평가 방법별 영업권 가치 비교'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # 다운로드 버튼 (실제로는 아직 기능 없음)
    st.download_button(
        label="PDF 보고서 다운로드",
        data="샘플 PDF 데이터",  # 실제로는 PDF 파일 생성 필요
        file_name=f"{st.session_state.company_data.get('name')}_영업권평가보고서.pdf",
        mime="application/pdf",
        disabled=True  # Phase 3에서 활성화 예정
    )

# 메인 함수
def main():
    # 사이드바 렌더링
    render_sidebar()
    
    # 현재 페이지에 따라 다른 함수 호출
    if st.session_state.current_page == 'home':
        home_page()
    elif st.session_state.current_page == 'company_info':
        company_info_page()
    elif st.session_state.current_page == 'excess_earnings':
        excess_earnings_page()
    elif st.session_state.current_page == 'dcf':
        dcf_page()
    elif st.session_state.current_page == 'market_comparison':
        market_comparison_page()
    elif st.session_state.current_page == 'results':
        results_page()
    elif st.session_state.current_page == 'report':
        report_page()

if __name__ == "__main__":
    main() 