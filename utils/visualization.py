import plotly.graph_objects as go
import pandas as pd

def create_loan_payment_chart(df):
    """대출 상환 스케줄에 대한 차트를 생성합니다"""
    fig = go.Figure()
    
    # 원금 상환 부분
    fig.add_trace(go.Bar(
        x=df.index, 
        y=df['원금상환'],
        name='원금상환',
        marker_color='#2E86C1'
    ))
    
    # 이자 부분
    fig.add_trace(go.Bar(
        x=df.index, 
        y=df['이자금액'],
        name='이자금액',
        marker_color='#F39C12'
    ))
    
    # 잔금 라인
    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['잔금'],
        name='잔금',
        mode='lines',
        line=dict(color='#E74C3C', width=3)
    ))
    
    fig.update_layout(
        title='대출 상환 스케줄',
        xaxis_title='납입회차',
        yaxis_title='금액 (원)',
        barmode='stack',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig
