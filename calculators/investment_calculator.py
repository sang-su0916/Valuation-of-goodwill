import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def investment_calculator():
    st.header("투자계산기")
    
    # 사용 방법 안내
    with st.expander("💡 투자계산기 사용 방법"):
        st.write("""
        이 투자계산기는 두 가지 핵심 계산을 제공합니다:
        
        **미래가치(FV) 계산**: 현재 투자금액이 미래에 얼마가 될지 계산합니다.
        - 예: 현재 1천만원과 매월 50만원을 연 7%로 10년간 투자하면 얼마가 될까요?
        
        **현재가치(PV) 계산**: 미래에 필요한 금액을 위해 현재 얼마를 투자해야 할지 계산합니다.
        - 예: 10년 후 1억원이 필요하다면, 연 7%로 투자할 때 현재 얼마를 준비해야 할까요?
        
        **계산 방식 설명**:
        - 미래가치(FV) = 초기투자금 × (1 + 이율)^기간 + 정기납입금 × [(1 + 이율)^기간 - 1] ÷ 이율
        - 현재가치(PV) = 목표금액 ÷ (1 + 이율)^기간 - 정기납입금 × [(1 + 이율)^기간 - 1] ÷ [이율 × (1 + 이율)^기간]
        """)
    
    # 계산 유형 선택
    calc_type = st.radio(
        "계산 유형",
        options=["미래가치(FV) 계산", "현재가치(PV) 계산"],
        horizontal=True
    )
    
    # 탭으로 기본 입력과 상세 설정 분리
    tabs = st.tabs(["기본 입력", "상세 설정"])
    
    with tabs[0]:
        col1, col2 = st.columns(2)
        
        with col1:
            if calc_type == "미래가치(FV) 계산":
                initial_investment_text = st.text_input(
                    "초기투자금액 (원)",
                    value="10,000,000",
                    help="처음에 한 번 투자하는 금액"
                )
                try:
                    initial_investment = int(initial_investment_text.replace(',', ''))
                except:
                    initial_investment = 10000000
            else:
                target_amount_text = st.text_input(
                    "목표금액 (원)",
                    value="100,000,000",
                    help="미래에 달성하고자 하는 목표 금액"
                )
                try:
                    target_amount = int(target_amount_text.replace(',', ''))
                except:
                    target_amount = 100000000
                
            monthly_contribution_text = st.text_input(
                "정기 투자금액 (원)",
                value="500,000",
                help="정기적으로 추가 투자하는 금액"
            )
            try:
                monthly_contribution = int(monthly_contribution_text.replace(',', ''))
            except:
                monthly_contribution = 500000
            
            # 정기 투자 주기 선택
            contribution_period = st.radio(
                "투자 주기",
                options=["월 납입", "연 납입"],
                horizontal=True,
                index=0
            )
        
        with col2:
            # 투자 기간 단위 선택
            period_unit = st.radio(
                "투자 기간 단위",
                options=["년", "월"],
                horizontal=True,
                index=0
            )
            
            if period_unit == "년":
                investment_period = st.number_input(
                    "투자기간 (년)",
                    min_value=1,
                    max_value=50,
                    value=10
                )
                total_months = investment_period * 12
            else:
                investment_period = st.number_input(
                    "투자기간 (월)",
                    min_value=1,
                    max_value=600,
                    value=120
                )
                total_months = investment_period
            
            # 이율 단위 선택
            rate_unit = st.radio(
                "수익률 단위",
                options=["연이율", "월이율"],
                horizontal=True,
                index=0
            )
            
            if rate_unit == "연이율":
                annual_return = st.number_input(
                    "연수익률 (%)",
                    min_value=0.0,
                    max_value=30.0,
                    value=7.0,
                    step=0.5
                )
                monthly_rate = annual_return / 12 / 100
            else:
                monthly_return = st.number_input(
                    "월수익률 (%)",
                    min_value=0.0,
                    max_value=5.0,
                    value=0.6,
                    step=0.1
                )
                monthly_rate = monthly_return / 100
                annual_return = monthly_rate * 12 * 100
    
    with tabs[1]:
        col1, col2 = st.columns(2)
        
        with col1:
            # 복리 계산 주기 선택
            compound_freq = st.selectbox(
                "복리 계산 주기",
                options=["월 복리", "분기 복리", "반기 복리", "연 복리"],
                index=0,
                help="이자가 원금에 합산되는 주기"
            )
            
            if compound_freq == "월 복리":
                compounding_periods = 12
            elif compound_freq == "분기 복리":
                compounding_periods = 4
            elif compound_freq == "반기 복리":
                compounding_periods = 2
            else:  # 연 복리
                compounding_periods = 1
            
            # 인플레이션 고려
            consider_inflation = st.checkbox("인플레이션 고려", value=False)
            
            if consider_inflation:
                inflation_rate = st.slider(
                    "인플레이션율 (%/년)",
                    min_value=0.0,
                    max_value=10.0,
                    value=2.0,
                    step=0.1
                )
            else:
                inflation_rate = 0.0
        
        with col2:
            # 세금 고려
            consider_tax = st.checkbox("세금 고려", value=False)
            
            if consider_tax:
                tax_rate = st.slider(
                    "세율 (%)",
                    min_value=0.0,
                    max_value=50.0,
                    value=15.4,
                    help="금융투자소득세율 (기본 15.4%)"
                )
            else:
                tax_rate = 0.0
            
            # 추가 설정
            show_real_value = st.checkbox(
                "실질 가치 표시",
                value=True,
                help="인플레이션을 고려한 실질 가치 표시"
            ) if consider_inflation else False
    
    # 조정된 월이율 계산 (복리 주기에 따라)
    if compounding_periods < 12:
        # 연이율을 복리 주기에 맞게 변환
        periodic_rate = annual_return / 100 / compounding_periods
        # 월별 유효이율 계산 (월 단위 복리 아닐 경우)
        effective_monthly_rate = (1 + periodic_rate) ** (1 / (12 / compounding_periods)) - 1
    else:
        effective_monthly_rate = monthly_rate
    
    # 실질 수익률 계산 (인플레이션 고려)
    if consider_inflation:
        real_annual_return = ((1 + annual_return/100) / (1 + inflation_rate/100) - 1) * 100
        real_monthly_rate = ((1 + effective_monthly_rate) / (1 + inflation_rate/100/12) - 1)
    else:
        real_annual_return = annual_return
        real_monthly_rate = effective_monthly_rate
    
    # 세후 수익률 계산
    if consider_tax:
        after_tax_annual_return = annual_return * (1 - tax_rate/100)
        after_tax_monthly_rate = effective_monthly_rate * (1 - tax_rate/100)
    else:
        after_tax_annual_return = annual_return
        after_tax_monthly_rate = effective_monthly_rate
    
    if st.button("계산하기", key="investment_button", use_container_width=True):
        # 투자 주기에 따른 기여금 조정
        if contribution_period == "연 납입":
            # 연간 납입액을 월간 등가로 변환
            monthly_equivalent = monthly_contribution / 12
        else:
            monthly_equivalent = monthly_contribution
        
        # 세전 계산
        if calc_type == "미래가치(FV) 계산":
            # 미래가치 계산
            future_value = calculate_future_value(initial_investment, monthly_equivalent, effective_monthly_rate, total_months)
            
            # 총 투자금액 계산
            if contribution_period == "월 납입":
                total_contributions = initial_investment + monthly_contribution * total_months
            else:  # 연 납입
                total_contributions = initial_investment + monthly_contribution * (total_months / 12)
                
            investment_gain = future_value - total_contributions
            
            # 세후 미래가치 계산
            if consider_tax:
                taxable_amount = investment_gain
                tax_amount = taxable_amount * (tax_rate / 100)
                after_tax_future_value = future_value - tax_amount
            else:
                after_tax_future_value = future_value
                tax_amount = 0
                
            # 실질 가치 계산 (인플레이션 고려)
            if consider_inflation:
                real_value_factor = (1 + inflation_rate/100) ** (total_months/12)
                real_future_value = after_tax_future_value / real_value_factor
            else:
                real_future_value = after_tax_future_value
            
            # 내부수익률 계산
            if total_contributions > 0:
                roi = ((future_value / total_contributions) ** (12 / total_months) - 1) * 12 * 100
            else:
                roi = 0
                
            # 결과 표시: 탭 사용
            result_tabs = st.tabs(["요약", "상세 분석", "시각화"])
            
            with result_tabs[0]:
                st.subheader("투자 결과 요약")
                
                result_cols = st.columns(3)
                with result_cols[0]:
                    st.metric("미래 가치", f"₩{future_value:,.0f}")
                    if consider_tax:
                        st.metric("세후 미래 가치", f"₩{after_tax_future_value:,.0f}")
                    if consider_inflation:
                        st.metric("실질 미래 가치", f"₩{real_future_value:,.0f}", 
                                 f"인플레이션 조정 {real_future_value/future_value*100:.1f}%")
                
                with result_cols[1]:
                    st.metric("총 투자금액", f"₩{total_contributions:,.0f}")
                    st.metric("투자 수익", f"₩{investment_gain:,.0f}", 
                             f"투자금 대비 {investment_gain/total_contributions*100:.1f}%")
                    if consider_tax:
                        st.metric("세금", f"₩{tax_amount:,.0f}", f"{tax_rate:.1f}%")
                
                with result_cols[2]:
                    st.metric("투자 기간", f"{investment_period} {period_unit}")
                    st.metric("내부수익률", f"{roi:.2f}%/년")
                    st.metric("수익 배수", f"{future_value/total_contributions:.2f}배")
                
                # 직관적 설명
                st.markdown("---")
                st.markdown(f"""
                ### 💡 직관적인 결과 설명
                
                현재 **₩{initial_investment:,}**를 투자하고, 매{contribution_period[0]} **₩{monthly_contribution:,}**씩 {investment_period}{period_unit} 동안 투자하면:
                
                - **총 납입금액**: ₩{total_contributions:,}
                - **최종 자산**: ₩{future_value:,} (원금의 {future_value/total_contributions:.2f}배)
                - **투자 수익**: ₩{investment_gain:,} (연평균 {roi:.2f}% 수익률)
                
                🔹 초기 투자금 **₩{initial_investment:,}**는 {investment_period}{period_unit} 후 **₩{initial_investment*(1+effective_monthly_rate)**total_months:,.0f}**로 성장
                🔹 매{contribution_period[0]} 납입금 **₩{monthly_contribution:,}**은 총 **₩{future_value-initial_investment*(1+effective_monthly_rate)**total_months:,.0f}**로 성장
                """)
                
                if consider_tax:
                    st.markdown(f"🔹 세금 **₩{tax_amount:,}**을 납부하면 최종 금액은 **₩{after_tax_future_value:,}**")
                
                if consider_inflation:
                    st.markdown(f"🔹 물가상승률 {inflation_rate:.1f}%를 고려하면 실질 가치는 **₩{real_future_value:,.0f}** (현재 가치 기준)")
                
            with result_tabs[1]:
                st.subheader("상세 분석")
                
                # 연도별 투자 현황
                df = generate_investment_data(
                    initial_investment, 
                    monthly_equivalent, 
                    effective_monthly_rate, 
                    total_months, 
                    contribution_period
                )
                
                # 표시 간격 선택
                display_interval = st.selectbox(
                    "표시 간격",
                    options=["연도별", "월별", "분기별"],
                    index=0
                )
                
                if display_interval == "연도별":
                    display_df = df[df['월'] % 12 == 0].copy()
                    display_df['기간'] = display_df['월'] // 12
                    display_df['단위'] = "년"
                elif display_interval == "분기별":
                    display_df = df[df['월'] % 3 == 0].copy()
                    display_df['기간'] = display_df['월'] // 3
                    display_df['단위'] = "분기"
                else:  # 월별
                    display_df = df.copy()
                    display_df['기간'] = display_df['월']
                    display_df['단위'] = "월"
                
                # 실질 가치 및 세후 가치 계산
                if consider_inflation or consider_tax:
                    display_df['세후 총자산'] = display_df['총자산']
                    
                    if consider_tax:
                        display_df['세후 투자수익'] = display_df['투자수익'] * (1 - tax_rate/100)
                        display_df['세후 총자산'] = display_df['투자원금'] + display_df['세후 투자수익']
                    
                    if consider_inflation:
                        display_df['인플레이션 계수'] = (1 + inflation_rate/100) ** (display_df['월']/12)
                        display_df['실질 총자산'] = display_df['세후 총자산'] / display_df['인플레이션 계수']
                
                # 표시할 컬럼 선택
                display_columns = ['기간', '단위', '투자원금', '투자수익', '총자산']
                if consider_tax:
                    display_columns.extend(['세후 투자수익', '세후 총자산'])
                if consider_inflation:
                    display_columns.append('실질 총자산')
                
                display_df = display_df[display_columns].copy()
                
                # 숫자 포맷팅
                for col in display_columns:
                    if col not in ['기간', '단위']:
                        display_df[col] = display_df[col].map('{:,.0f}'.format)
                
                st.dataframe(display_df, use_container_width=True)
                
                # 주요 이정표 표시
                st.subheader("주요 이정표")
                
                # 원금 2배, 5배, 10배 지점 찾기
                milestones = []
                multipliers = [2, 5, 10]
                
                for multiplier in multipliers:
                    target_value = total_contributions * multiplier
                    if future_value >= target_value:
                        for i in range(len(df)-1):
                            if df.iloc[i]['총자산'] < target_value <= df.iloc[i+1]['총자산']:
                                milestone_month = df.iloc[i+1]['월']
                                milestones.append({
                                    "배수": multiplier,
                                    "금액": target_value,
                                    "도달시점": f"{milestone_month//12}년 {milestone_month%12}개월",
                                    "월": milestone_month
                                })
                                break
                
                if milestones:
                    milestone_df = pd.DataFrame(milestones)
                    milestone_df["금액"] = milestone_df["금액"].map('{:,.0f}'.format)
                    st.table(milestone_df[["배수", "금액", "도달시점"]])
                else:
                    st.write("투자금의 2배 이상 도달 시점이 계산 기간 내에 없습니다.")
                
                # 이율 정보 표시
                st.subheader("이율 정보")
                rate_cols = st.columns(4)
                with rate_cols[0]:
                    st.metric("명목 연이율", f"{annual_return:.2f}%")
                with rate_cols[1]:
                    st.metric("유효 월이율", f"{effective_monthly_rate*100:.4f}%")
                with rate_cols[2]:
                    if consider_inflation:
                        st.metric("실질 연이율", f"{real_annual_return:.2f}%", 
                                 f"인플레이션 {inflation_rate:.1f}% 고려")
                with rate_cols[3]:
                    if consider_tax:
                        st.metric("세후 연이율", f"{after_tax_annual_return:.2f}%", 
                                 f"세율 {tax_rate:.1f}% 적용")
            
            with result_tabs[2]:
                st.subheader("투자 성장 시각화")
                
                # 그래프 생성
                fig = go.Figure()
                
                # 연도별 데이터 준비
                yearly_df = df[df['월'] % 12 == 0].copy()
                
                # 투자 원금 영역
                fig.add_trace(go.Scatter(
                    x=yearly_df['월'] / 12,
                    y=yearly_df['투자원금'],
                    fill='tozeroy',
                    mode='lines',
                    name='투자 원금',
                    line=dict(color='#3498db')
                ))
                
                # 투자 수익 영역
                fig.add_trace(go.Scatter(
                    x=yearly_df['월'] / 12,
                    y=yearly_df['총자산'],
                    fill='tonexty',
                    mode='lines',
                    name='투자 수익',
                    line=dict(color='#2ecc71')
                ))
                
                # 세후 총자산 선
                if consider_tax:
                    yearly_df['세후 투자수익'] = yearly_df['투자수익'] * (1 - tax_rate/100)
                    yearly_df['세후 총자산'] = yearly_df['투자원금'] + yearly_df['세후 투자수익']
                    
                    fig.add_trace(go.Scatter(
                        x=yearly_df['월'] / 12,
                        y=yearly_df['세후 총자산'],
                        mode='lines',
                        name='세후 자산',
                        line=dict(color='#e74c3c', dash='dash')
                    ))
                
                # 실질 가치 선
                if consider_inflation:
                    yearly_df['인플레이션 계수'] = (1 + inflation_rate/100) ** (yearly_df['월']/12)
                    if consider_tax:
                        yearly_df['실질 총자산'] = yearly_df['세후 총자산'] / yearly_df['인플레이션 계수']
                    else:
                        yearly_df['실질 총자산'] = yearly_df['총자산'] / yearly_df['인플레이션 계수']
                        
                    fig.add_trace(go.Scatter(
                        x=yearly_df['월'] / 12,
                        y=yearly_df['실질 총자산'],
                        mode='lines',
                        name='실질 가치',
                        line=dict(color='#9b59b6', dash='dot')
                    ))
                
                # 그래프 레이아웃 설정
                fig.update_layout(
                    title='연도별 투자 성장',
                    xaxis_title='투자 기간 (년)',
                    yaxis_title='금액 (원)',
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                # 그래프 표시
                st.plotly_chart(fig, use_container_width=True)
                
                # 원금 대비 수익 비율 그래프
                st.subheader("원금 대비 수익 비율")
                
                yearly_df['수익률'] = (yearly_df['총자산'] / yearly_df['투자원금'] - 1) * 100
                
                fig2 = go.Figure()
                
                fig2.add_trace(go.Bar(
                    x=yearly_df['월'] / 12,
                    y=yearly_df['수익률'],
                    name='수익률 (%)',
                    marker_color='#f39c12'
                ))
                
                fig2.update_layout(
                    xaxis_title='투자 기간 (년)',
                    yaxis_title='수익률 (%)',
                )
                
                st.plotly_chart(fig2, use_container_width=True)
                
        else:  # 현재가치(PV) 계산
            # 현재가치 계산
            present_value = calculate_present_value(target_amount, monthly_equivalent, effective_monthly_rate, total_months)
            
            # 총 기여금 계산
            if contribution_period == "월 납입":
                total_contributions = monthly_contribution * total_months
            else:  # 연 납입
                total_contributions = monthly_contribution * (total_months / 12)
                
            total_required = present_value + total_contributions
            future_gain = target_amount - total_required
            
            # 내부수익률 계산
            if total_required > 0:
                roi = ((target_amount / total_required) ** (12 / total_months) - 1) * 12 * 100
            else:
                roi = 0
            
            # 결과 표시: 탭 사용
            result_tabs = st.tabs(["요약", "상세 분석", "시각화"])
            
            with result_tabs[0]:
                st.subheader("투자 결과 요약")
                
                result_cols = st.columns(3)
                with result_cols[0]:
                    st.metric("필요 초기 투자금", f"₩{present_value:,.0f}")
                    st.metric("목표 금액", f"₩{target_amount:,.0f}")
                
                with result_cols[1]:
                    st.metric("총 정기 투자액", f"₩{total_contributions:,.0f}")
                    st.metric("총 필요 자금", f"₩{total_required:,.0f}")
                
                with result_cols[2]:
                    st.metric("투자 수익", f"₩{future_gain:,.0f}", 
                             f"{future_gain/total_required*100:.1f}%")
                    st.metric("내부수익률", f"{roi:.2f}%/년")
                
                # 직관적 설명
                st.markdown("---")
                st.markdown(f"""
                ### 💡 직관적인 결과 설명
                
                {investment_period}{period_unit} 후 **₩{target_amount:,}**를 만들기 위해서는:
                
                - **초기 투자금**: ₩{present_value:,}
                - **정기 투자**: 매{contribution_period[0]} ₩{monthly_contribution:,}씩 {investment_period}{period_unit} 동안
                - **총 투자 자금**: ₩{total_required:,}
                - **투자 수익**: ₩{future_gain:,} (연평균 {roi:.2f}% 수익률)
                
                🔹 초기 투자금 **₩{present_value:,}**는 {investment_period}{period_unit} 후 **₩{present_value*(1+effective_monthly_rate)**total_months:,.0f}**로 성장
                🔹 매{contribution_period[0]} 납입금 **₩{monthly_contribution:,}**은 총 **₩{target_amount-present_value*(1+effective_monthly_rate)**total_months:,.0f}**로 성장
                """)
                
                if consider_inflation:
                    real_target = target_amount * ((1 + inflation_rate/100) ** (total_months/12))
                    st.markdown(f"🔹 인플레이션 {inflation_rate:.1f}%를 고려하면 실제 필요한 금액은 **₩{real_target:,.0f}** (미래 화폐가치 기준)")
            
            with result_tabs[1]:
                st.subheader("목표 달성을 위한 대안 시나리오")
                
                # 다양한 조합으로 목표 달성하는 방법 제시
                st.write("다음은 다양한 초기 투자금과 정기 납입금 조합으로 목표를 달성하는 방법입니다:")
                
                scenarios = []
                initial_percentages = [0, 25, 50, 75, 100]
                
                for pct in initial_percentages:
                    # 초기 투자금 비율에 따른 금액
                    scenario_initial = target_amount * (pct / 100) / ((1 + effective_monthly_rate) ** total_months)
                    
                    # 필요한 월 납입액 계산
                    if effective_monthly_rate > 0:
                        scenario_monthly = (target_amount - scenario_initial * ((1 + effective_monthly_rate) ** total_months)) / (((1 + effective_monthly_rate) ** total_months - 1) / effective_monthly_rate)
                    else:
                        scenario_monthly = (target_amount - scenario_initial) / total_months
                    
                    if scenario_monthly >= 0:
                        # 총 투자금액
                        total_investment = scenario_initial + scenario_monthly * total_months
                        # 투자 수익
                        investment_gain = target_amount - total_investment
                        # 수익률
                        if total_investment > 0:
                            scenario_roi = ((target_amount / total_investment) ** (12 / total_months) - 1) * 12 * 100
                        else:
                            scenario_roi = 0
                            
                        scenarios.append({
                            "초기 투자 비율": f"{pct}%",
                            "초기 투자금": int(scenario_initial),
                            "월 납입금": int(scenario_monthly),
                            "총 투자액": int(total_investment),
                            "투자 수익": int(investment_gain),
                            "수익률": scenario_roi
                        })
                
                # 시나리오 데이터프레임 생성 및 표시
                scenario_df = pd.DataFrame(scenarios)
                
                # 숫자 포맷팅
                for col in ["초기 투자금", "월 납입금", "총 투자액", "투자 수익"]:
                    scenario_df[col] = scenario_df[col].map('{:,.0f}'.format)
                
                scenario_df["수익률"] = scenario_df["수익률"].map('{:.2f}%'.format)
                
                st.table(scenario_
