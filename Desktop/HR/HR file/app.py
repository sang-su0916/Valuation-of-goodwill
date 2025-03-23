import streamlit as st
import os
import sys
from streamlit_option_menu import option_menu
from PIL import Image
import base64

# 모듈 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 각 모듈 임포트
from annual_leave_ui import render_annual_leave_calculator
from employment_contract import render_employment_contract_form
from payroll_ledger import render_payroll_ledger_ui
from pay_statement import render_pay_statement_ui

# 페이지 설정
st.set_page_config(
    page_title="HR 관리 시스템",
    page_icon="👨‍💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 적용
def load_css():
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Noto Sans KR', sans-serif;
        }
        
        .main-header {
            font-size: 2.5rem;
            color: #1E88E5;
            text-align: center;
            margin-bottom: 1.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #1976D2, #64B5F6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            padding: 0.5rem;
            border-bottom: 2px solid #E3F2FD;
        }
        
        .sub-header {
            font-size: 1.8rem;
            color: #1976D2;
            margin-bottom: 1.2rem;
            font-weight: 500;
            border-left: 4px solid #1976D2;
            padding-left: 0.8rem;
        }
        
        .info-box {
            background-color: #E3F2FD;
            padding: 1.2rem;
            border-radius: 0.8rem;
            margin-bottom: 1.5rem;
            border-left: 5px solid #1976D2;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 4rem;
            white-space: pre-wrap;
            background-color: #F5F5F5;
            border-radius: 0.8rem 0.8rem 0 0;
            padding: 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #1E88E5 !important;
            color: white !important;
            font-weight: 700 !important;
            transform: translateY(-3px);
            box-shadow: 0 3px 10px rgba(30, 136, 229, 0.3);
        }
        
        div[data-testid="stSidebarNav"] {
            background-image: linear-gradient(135deg, #1E88E5, #64B5F6);
            padding-top: 2rem;
            border-radius: 0.8rem;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
        }
        
        div[data-testid="stSidebarNav"] li {
            margin-bottom: 0.8rem;
        }
        
        div[data-testid="stSidebarNav"] li > div {
            border-radius: 0.5rem;
            padding: 0.8rem;
            transition: all 0.2s ease;
        }
        
        div[data-testid="stSidebarNav"] li > div:hover {
            background-color: rgba(255, 255, 255, 0.3);
            transform: translateX(5px);
        }
        
        div[data-testid="stSidebarNav"] li > div[aria-selected="true"] {
            background-color: rgba(255, 255, 255, 0.4);
            border-left: 3px solid white;
        }
        
        div[data-testid="stSidebarNav"] span {
            color: white;
            font-weight: 500;
        }
        
        div[data-testid="stSidebarNav"] span:hover {
            color: white;
        }
        
        div[data-testid="stForm"] {
            background-color: #F5F5F5;
            padding: 1.8rem;
            border-radius: 0.8rem;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
            border: 1px solid #E0E0E0;
        }
        
        div[data-testid="stFormSubmitButton"] > button {
            background-color: #1E88E5;
            color: white;
            font-weight: 500;
            border-radius: 0.5rem;
            padding: 0.6rem 2.5rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(30, 136, 229, 0.3);
        }
        
        div[data-testid="stFormSubmitButton"] > button:hover {
            background-color: #1565C0;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(30, 136, 229, 0.4);
        }
        
        div[data-testid="metric-container"] {
            background-color: white;
            border-radius: 0.8rem;
            padding: 1.5rem;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
            border: 1px solid #E0E0E0;
            transition: all 0.3s ease;
        }
        
        div[data-testid="metric-container"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            border-color: #64B5F6;
        }
        
        div[data-testid="stDataFrame"] {
            border-radius: 0.8rem;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        div[data-testid="stDataFrame"] table {
            border-collapse: collapse;
        }
        
        div[data-testid="stDataFrame"] th {
            background-color: #1976D2;
            color: white;
            font-weight: 500;
            padding: 0.8rem;
            text-align: center;
        }
        
        div[data-testid="stDataFrame"] td {
            padding: 0.8rem;
            text-align: center;
            border-bottom: 1px solid #EEEEEE;
        }
        
        div[data-testid="stDataFrame"] tr:nth-child(even) {
            background-color: #F5F5F5;
        }
        
        div[data-testid="stDataFrame"] tr:hover {
            background-color: #E3F2FD;
        }
        
        button[kind="primary"] {
            background-color: #1976D2;
            color: white;
            font-weight: 500;
            border-radius: 0.5rem;
            padding: 0.6rem 2rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(25, 118, 210, 0.3);
        }
        
        button[kind="primary"]:hover {
            background-color: #1565C0;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(25, 118, 210, 0.4);
        }
        
        button[kind="secondary"] {
            background-color: white;
            color: #1976D2;
            font-weight: 500;
            border-radius: 0.5rem;
            padding: 0.6rem 2rem;
            border: 1px solid #1976D2;
            transition: all 0.3s ease;
        }
        
        button[kind="secondary"]:hover {
            background-color: #E3F2FD;
            color: #1565C0;
            border-color: #1565C0;
        }
        
        .stDownloadButton > button {
            background-color: #4CAF50;
            color: white;
            font-weight: 500;
            border-radius: 0.5rem;
            padding: 0.6rem 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(76, 175, 80, 0.3);
        }
        
        .stDownloadButton > button:hover {
            background-color: #43A047;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(76, 175, 80, 0.4);
        }
        
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid #EEEEEE;
            color: #757575;
            font-size: 0.9rem;
        }
        
        /* 반응형 디자인 개선 */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2rem;
            }
            
            .sub-header {
                font-size: 1.5rem;
            }
            
            div[data-testid="stForm"] {
                padding: 1rem;
            }
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# 배경 이미지 설정
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    bg_image = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    
    st.markdown(bg_image, unsafe_allow_html=True)

# 배경 이미지 파일 생성
def create_background_image():
    # 배경 이미지 디렉토리 생성
    image_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/images")
    os.makedirs(image_dir, exist_ok=True)
    
    # 배경 이미지 파일 경로
    bg_image_path = os.path.join(image_dir, "background.png")
    
    # 배경 이미지가 없는 경우 생성
    if not os.path.exists(bg_image_path):
        # 모던한 그라데이션 배경 이미지 생성
        from PIL import Image, ImageDraw
        
        width, height = 1920, 1080
        image = Image.new("RGBA", (width, height), color=(255, 255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # 그라데이션 색상 정의 (하늘색 - 파란색 그라데이션)
        colors = [
            (240, 249, 255),  # 매우 밝은 하늘색
            (224, 240, 255),  # 밝은 하늘색
            (214, 234, 248),  # 하늘색
            (198, 219, 240),  # 중간 하늘색
            (187, 210, 236),  # 진한 하늘색
            (179, 205, 233)   # 가장 진한 하늘색
        ]
        
        # 그라데이션 효과 생성 (상단에서 하단으로)
        segment_height = height / (len(colors) - 1)
        
        for i in range(len(colors) - 1):
            start_color = colors[i]
            end_color = colors[i + 1]
            start_y = int(i * segment_height)
            end_y = int((i + 1) * segment_height)
            
            for y in range(start_y, end_y):
                # 두 색상 사이의 보간
                ratio = (y - start_y) / segment_height
                r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
                g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
                b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
                
                draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        
        # 대각선 패턴 추가 (오른쪽 상단에서 왼쪽 하단으로)
        for i in range(0, width + height, 40):
            start_point = (min(i, width), max(0, i - width))
            end_point = (max(0, i - height), min(i, height))
            
            # 패턴 라인 그리기 (매우 옅은 파란색)
            draw.line([start_point, end_point], fill=(255, 255, 255, 20), width=2)
        
        # 이미지 저장
        image.save(bg_image_path)
    
    return bg_image_path

# 메인 함수
def main():
    # CSS 스타일 적용
    load_css()
    
    # 배경 이미지 설정
    bg_image_path = create_background_image()
    add_bg_from_local(bg_image_path)
    
    # 세션 상태 초기화
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "홈"
    
    # 사이드바 메뉴
    with st.sidebar:
        st.title("HR 관리 시스템")
        
        selected = option_menu(
            menu_title=None,
            options=["홈", "연차휴가 계산기", "근로계약서", "임금대장", "임금명세서"],
            icons=["house", "calendar-check", "file-earmark-text", "cash-coin", "envelope"],
            menu_icon="cast",
            default_index=["홈", "연차휴가 계산기", "근로계약서", "임금대장", "임금명세서"].index(st.session_state.current_page),
        )
        
        st.session_state.current_page = selected
    
    # 페이지 렌더링
    if st.session_state.current_page == "홈":
        render_home_page()
    elif st.session_state.current_page == "연차휴가 계산기":
        render_annual_leave_calculator()
    elif st.session_state.current_page == "근로계약서":
        render_employment_contract_form()
    elif st.session_state.current_page == "임금대장":
        render_payroll_ledger_ui()
    elif st.session_state.current_page == "임금명세서":
        render_pay_statement_ui()
    
    # 푸터
    st.markdown(
        """
        <div class="footer">
            <p>© 2025 HR 관리 시스템 | 모든 권리 보유</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# 홈 페이지 렌더링
def render_home_page():
    st.markdown('<h1 class="main-header">HR 관리 시스템</h1>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="info-box">
            <h2 class="sub-header" style="margin-top:0">👋 환영합니다!</h2>
            <p style="font-size:18px; line-height:1.6">
                HR 관리 시스템은 인사 관리 업무를 효율적으로 처리할 수 있도록 도와주는 종합 솔루션입니다.
                연차휴가 계산, 근로계약서 작성, 임금대장 관리, 임금명세서 생성 등 다양한 기능을 제공합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 기능 소개
    st.markdown('<h2 class="sub-header">📊 주요 기능</h2>', unsafe_allow_html=True)
    
    # 카드 스타일 추가
    st.markdown(
        """
        <style>
        .feature-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            border-left: 5px solid #1976D2;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        .feature-title {
            color: #1976D2;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .feature-list {
            color: #424242;
            font-size: 16px;
            line-height: 1.6;
            list-style-type: none;
            padding-left: 15px;
        }
        .feature-list li {
            margin-bottom: 8px;
            position: relative;
        }
        .feature-list li:before {
            content: "✓";
            color: #4CAF50;
            position: absolute;
            left: -15px;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">🗓️ 연차휴가 계산기</div>
                <ul class="feature-list">
                    <li>입사일 기준 연차휴가 계산</li>
                    <li>회계연도 기준 연차휴가 계산</li>
                    <li>연차휴가 발생 테이블 생성</li>
                </ul>
            </div>
            
            <div class="feature-card">
                <div class="feature-title">📝 근로계약서</div>
                <ul class="feature-list">
                    <li>근로계약서 템플릿 제공</li>
                    <li>맞춤형 근로계약서 작성</li>
                    <li>PDF 형식으로 다운로드</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">💰 임금대장</div>
                <ul class="feature-list">
                    <li>직원 정보 관리</li>
                    <li>임금 지급 기록 관리</li>
                    <li>월별/연간 보고서 생성</li>
                </ul>
            </div>
            
            <div class="feature-card">
                <div class="feature-title">💵 임금명세서</div>
                <ul class="feature-list">
                    <li>개별 임금명세서 생성</li>
                    <li>일괄 임금명세서 생성</li>
                    <li>PDF 형식으로 다운로드</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # 시작하기
    st.markdown('<h2 class="sub-header">🚀 시작하기</h2>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="background-color:white; padding:20px; border-radius:10px; box-shadow:0 3px 10px rgba(0,0,0,0.1);">
            <p style="font-size:17px; line-height:1.6;">
                왼쪽 사이드바에서 원하는 기능을 선택하여 시작하세요.
            </p>
            <ul style="font-size:16px; line-height:1.6;">
                <li><b>연차휴가 계산기</b>: 직원의 연차휴가를 계산합니다.</li>
                <li><b>근로계약서</b>: 근로계약서를 작성하고 PDF로 다운로드합니다.</li>
                <li><b>임금대장</b>: 직원 정보와 임금 지급 기록을 관리합니다.</li>
                <li><b>임금명세서</b>: 임금명세서를 생성하고 PDF로 다운로드합니다.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 사용 팁
    st.markdown('<h2 class="sub-header">💡 사용 팁</h2>', unsafe_allow_html=True)
    
    st.info(
        """
        <div style="font-size:16px; line-height:1.6;">
        <ul style="margin-bottom:0; padding-left:20px;">
            <li>모든 데이터는 로컬에 저장되며, 인터넷 연결 없이도 사용할 수 있습니다.</li>
            <li>PDF 파일은 다운로드 후 인쇄하거나 이메일로 전송할 수 있습니다.</li>
            <li>정기적으로 데이터를 백업하는 것을 권장합니다.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
