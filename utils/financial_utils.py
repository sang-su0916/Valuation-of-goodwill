import pandas as pd
import numpy as np

def calculate_loan_schedule(principal, periods, monthly_rate, payment_type):
    """
    대출 상환 스케줄을 계산합니다.
    
    Args:
        principal: 대출 원금
        periods: 총 납입 회차 (개월 수)
        monthly_rate: 월 이자율 (연이자율/12/100)
        payment_type: 상환방식 (원리금균등상환, 원금균등상환, 만기일시상환)
    
    Returns:
        DataFrame: 상환 스케줄 데이터프레임
    """
    schedule = []
    remaining = principal
    
    if payment_type == "원리금균등상환":
        # 원리금균등상환 - 매달 동일한 금액 납부
        if monthly_rate == 0:
            payment = principal / periods
        else:
            payment = principal * (monthly_rate * (1 + monthly_rate) ** periods) / ((1 + monthly_rate) ** periods - 1)
        
        for period in range(1, periods + 1):
            interest = remaining * monthly_rate
            principal_payment = payment - interest
            remaining -= principal_payment
            
            # 마지막 회차에는 반올림 오차로 인해 잔액이 음수가 될 수 있음
            if period == periods:
                if abs(remaining) < 1:  # 1원 미만이면 0으로 조정
                    remaining = 0
            
            schedule.append({
                "회차": period,
                "납입금액": payment,
                "원금상환": principal_payment,
                "이자금액": interest,
                "잔금": max(0, remaining)
            })
            
    elif payment_type == "원금균등상환":
        # 원금균등상환 - 매달 동일한 원금 상환
        principal_payment = principal / periods
        
        for period in range(1, periods + 1):
            interest = remaining * monthly_rate
            payment = principal_payment + interest
            remaining -= principal_payment
            
            schedule.append({
                "회차": period,
                "납입금액": payment,
                "원금상환": principal_payment,
                "이자금액": interest,
                "잔금": max(0, remaining)
            })
            
    elif payment_type == "만기일시상환":
        # 만기일시상환 - 이자만 납부하다가 마지막에 원금 상환
        for period in range(1, periods + 1):
            interest = remaining * monthly_rate
            
            if period == periods:
                principal_payment = principal
                payment = principal + interest
                remaining = 0
            else:
                principal_payment = 0
                payment = interest
            
            schedule.append({
                "회차": period,
                "납입금액": payment,
                "원금상환": principal_payment,
                "이자금액": interest,
                "잔금": remaining
            })
    
    return pd.DataFrame(schedule).set_index("회차")
