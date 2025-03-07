import streamlit as st
import pandas as pd
import numpy as np

def insurance_calculator():
    st.header("보장계산기")
    
    # 사용 방법 안내
    with st.expander("💡 보장계산기 사용 방법"):
        st.write("""
        이 계산기는 가족의 미래를 보장하기 위해 필요한 보험금을 계산해 드립니다:
        
        1. 개인 정보와 가족 상황을 입력하세요.
        2. 현재 보유한 보험 정보를 입력하세요.
        3. '계산하기' 버튼을 클릭하여 필요한 보장 금액을 확인하세요.
        """)
    
    # 기본 정보 입력
    st.subheader("가족 정보")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("가장의 현재 나이", min_value=20, max_value=80, value=40)
        dependents = st.number_input("자녀 수", min_value=0, max_value=10, value=2)
        spouse_exists = st.checkbox("배우자 유무", value=True)
        
        if spouse_exists:
            spouse_age = st.number_input("배우자의 나이", min_value=20, max_value=80, value=38)
            spouse_retirement_age = st.number_input("배우자의 은퇴 희망 나이", min_value=spouse_age, max_value=90, value=65)
    
    with col2:
        annual_income_text = st.text_input(
            "현재 연소득 (원)",
            value="60,000,000",
            help="숫자만 입력하세요. 예: 60000000"
        )
        try:
            annual_income = int(annual_income_text.replace(',', ''))
        except:
            annual_income = 60000000
        
        monthly_living_expenses_text = st.text_input(
            "월 생활비 (원)",
            value="3,000,000",
            help="숫자만 입력하세요. 예: 3000000"
        )
        try:
            monthly_living_expenses = int(monthly_living_expenses_text.replace(',', ''))
        except:
            monthly_living_expenses = 3000000
        
        current_debt_text = st.text_input(
            "현재 대출 잔액 (원)",
            value="200,000,000",
            help="숫자만 입력하세요. 예: 200000000"
        )
        try:
            current_debt = int(current_debt_text.replace(',', ''))
        except:
            current_debt = 200000000
    
    # 어린 자녀 정보
    if dependents > 0:
        st.subheader("자녀 정보")
        children_ages = []
        
        cols = st.columns(min(4, dependents))
        for i in range(dependents):
            with cols[i % len(cols)]:
                child_age = st.number_input(f"{i+1}번째 자녀 나이", min_value=0, max_value=30, value=min(i*3, 18))
                children_ages.append(child_age)
    
    # 현재 보험 정보
    st.subheader("현재 보험 정보")
    
    col1, col2 = st.columns(2)
    
    with col1:
        life_insurance_text = st.text_input(
            "생명보험 보장금액 (원)",
            value="100,000,000",
            help="숫자만 입력하세요. 예: 100000000"
        )
        try:
            life_insurance = int(life_insurance_text.replace(',', ''))
        except:
            life_insurance = 100000000
        
        disability_insurance_text = st.text_input(
            "소득보장보험 월 보장금액 (원)",
            value="0",
            help="숫자만 입력하세요. 예: 1000000"
        )
        try:
            disability_insurance = int(disability_insurance_text.replace(',', ''))
        except:
            disability_insurance = 0
    
    with col2:
        critical_illness_insurance_text = st.text_input(
            "중대질병보험 보장금액 (원)",
            value="50,000,000",
            help="숫자만 입력하세요. 예: 50000000"
        )
        try:
            critical_illness_insurance = int(critical_illness_insurance_text.replace(',', ''))
        except:
            critical_illness_insurance = 50000000
        
        savings_text = st.text_input(
            "비상자금 (원)",
            value="20,000,000",
            help="숫자만 입력하세요. 예: 20000000"
        )
        try:
            savings = int(savings_text.replace(',', ''))
        except:
            savings = 20000000
    
    if st.button("계산하기", key="insurance_button", use_container_width=True):
        # 필요 보장금 계산
        results = calculate_insurance_needs(
            age=age,
            annual_income=annual_income,
            monthly_expenses=monthly_living_expenses,
            dependents=dependents,
            children_ages=children_ages if dependents > 0 else [],
            spouse_exists=spouse_exists,
            spouse_age=spouse_age if spouse_exists else None,
            debt=current_debt,
            savings=savings
        )
        
        # 현재 보험 상태
        current_coverage = {
            "생명보험": life_insurance,
            "소득보장": disability_insurance * 12,  # 연간으로 변환
            "중대질병": critical_illness_insurance
        }
        
        # 보장 갭 계산
        coverage_gap = {
            category: results[category] - current_coverage.get(category, 0)
            for category in results
        }
        
        # 결과 표시
        st.subheader("보장 분석 결과")
        
        # 요약 정보
        total_needed = sum(results.values())
        total_current = sum(current_coverage.values())
        total_gap = total_needed - total_current
        
        col1, col2, col3 = st.columns(3)
        col1.metric("필요 총 보장액", f"₩{total_needed:,.0f}")
        col2.metric("현재 총 보장액", f"₩{total_current:,.0f}")
        
        if total_gap > 0:
            col3.metric("보장 부족액", f"₩{total_gap:,.0f}", delta=f"-{total_gap/total_needed*100:.1f}%", delta_color="inverse")
        else:
            col3.metric("보장 초과액", f"₩{-total_gap:,.0f}", delta=f"+{-total_gap/total_needed*100:.1f}%", delta_color="normal")
        
        # 상세 분석
        st.subheader("보장 유형별 분석")
        
        for category in results:
            need = results[category]
            current = current_coverage.get(category, 0)
            gap = coverage_gap[category]
            
            col1, col2, col3 = st.columns(3)
            col1.metric(f"{category} 필요액", f"₩{need:,.0f}")
            col2.metric(f"현재 {category}", f"₩{current:,.0f}")
            
            if gap > 0:
                col3.metric("부족액", f"₩{gap:,.0f}", delta=f"-{gap/need*100:.1f}%" if need > 0 else "", delta_color="inverse")
                st.warning(f"{category} 보장이 부족합니다. 추가 가입을 고려하세요.")
            else:
                col3.metric("초과액", f"₩{-gap:,.0f}", delta=f"+{-gap/need*100:.1f}%" if need > 0 else "", delta_color="normal")
                st.success(f"{category} 보장이 충분합니다.")
            
            st.write("---")
        
        # 조언
        st.subheader("보장 개선 제안")
        
        insufficient = [k for k, v in coverage_gap.items() if v > 0]
        if insufficient:
            for area in insufficient:
                if area == "생명보험":
                    st.write("- **생명보험**: 정기 생명보험으로 보장을 강화하세요. 특히 소득원이 되는 가장에게 중요합니다.")
                elif area == "소득보장":
                    st.write("- **소득보장**: 장기 장애 발생 시 소득을 대체할 수 있는 소득보장보험을 고려하세요.")
                elif area == "중대질병":
                    st.write("- **중대질병**: 암, 뇌졸중, 심근경색 등 중대 질병 발생 시 경제적 부담을 덜어줄 수 있는 보험을 검토하세요.")
        else:
            st.success("현재 모든 영역의 보장이 충분합니다. 정기적으로 상황 변화에 따라 재검토하세요.")

def calculate_insurance_needs(age, annual_income, monthly_expenses, dependents, children_ages, spouse_exists, spouse_age, debt, savings):
    """필요한 보험 보장금액을 계산합니다."""
    results = {}
    
    # 생명보험 필요액 (소득 대체 + 부채 + 자녀 교육비 - 저축)
    years_to_retirement = 65 - age
    income_replacement_years = min(years_to_retirement, 20)  # 최대 20년간 소득 대체
    income_replacement = annual_income * 0.7 * income_replacement_years  # 소득의 70%
    
    # 자녀 교육비 (대학교 4년 기준, 1인당 1억원 가정)
    education_costs = 0
    for child_age in children_ages:
        if child_age < 19:
            education_costs += 100000000  # 자녀당 1억원
    
    life_insurance_need = income_replacement + debt + education_costs - savings
    life_insurance_need = max(0, life_insurance_need)
    
    # 소득보장보험 필요액 (연간 소득의 60%)
    disability_need = annual_income * 0.6
    
    # 중대질병보험 필요액 (연간 소득의 3배 + 치료비 5천만원 가정)
    critical_illness_need = annual_income * 3 + 50000000
    
    results["생명보험"] = life_insurance_need
    results["소득보장"] = disability_need
    results["중대질병"] = critical_illness_need
    
    return results
