import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="영업권 평가 시스템",
    page_icon="💰"
)

# 메인 타이틀
st.title("영업권 평가 시스템")
st.write("배포 테스트 중입니다. 곧 정식 버전이 제공될 예정입니다.")

# 기본 정보 입력
st.header("평가 정보 입력")
company_name = st.text_input("회사명", "")
    
# 재무 정보 입력
st.subheader("재무 정보")
revenue = st.number_input("매출액 (백만원)", min_value=0.1, value=100.0)
operating_profit = st.number_input("영업이익 (백만원)", value=10.0)
    
# 성장률 및 할인율 입력
st.subheader("성장률 및 할인율")
growth_rate = st.slider("성장률 (%)", min_value=0.1, max_value=30.0, value=5.0)
discount_rate = st.slider("할인율 (%)", min_value=0.1, max_value=30.0, value=10.0)
    
# 계산 버튼
if st.button("평가 계산", type="primary"):
    # 간단한 계산만 진행
    goodwill_value = operating_profit * 5  # 매우 단순화된 계산
    st.success(f"영업권 평가액: {goodwill_value:,.0f} 백만원")
    st.info("상세 결과는 개발 중입니다.") 