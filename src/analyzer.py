import pandas as pd
import numpy as np
import yfinance as yf
import statsmodels.api as sm
import pandas_datareader.data as web
from datetime import datetime

def run_fama_french_analysis(portfolio_tickers):
    # 1. ดึงข้อมูลราคา
    raw_data = yf.download(portfolio_tickers, start="2020-01-01", end="2025-12-31")
    data = raw_data['Close'] if 'Adj Close' not in raw_data.columns else raw_data['Adj Close']

    # คำนวณผลตอบแทนรายเดือน และเปลี่ยน Index เป็น Period (Year-Month)
    port_ret = data.pct_change().mean(axis=1).resample('ME').apply(lambda x: (1 + x).prod() - 1)
    port_ret.index = port_ret.index.to_period('M') 
    port_ret = port_ret.to_frame('Portfolio_Ret')

    # 2. ดึง Fama-French Factors
    print("📡 Fetching Fama-French factors...")
    ff_factors = web.DataReader('F-F_Research_Data_Factors', 'famafrench', start='2020-01-01')[0]
    ff_factors = ff_factors / 100
    
    # เช็กก่อนแปลง: ถ้ายังไม่เป็น PeriodIndex ค่อยแปลง
    if not isinstance(ff_factors.index, pd.PeriodIndex):
        ff_factors.index = ff_factors.index.to_period('M')

    # 3. รวมข้อมูล (Join ด้วย Year-Month)
    df = port_ret.join(ff_factors, how='inner').dropna()
    print(f"✅ Data Synchronized: {len(df)} months of overlapping data found.")

    if len(df) == 0:
        raise ValueError("❌ No overlapping dates found! Check data start/end dates.")

    df['Excess_Ret'] = df['Portfolio_Ret'] - df['RF']

    # 4. รัน OLS Regression
    Y = df['Excess_Ret']
    X = df[['Mkt-RF', 'SMB', 'HML']]
    X = sm.add_constant(X)
    
    model = sm.OLS(Y, X).fit()
    return model

if __name__ == "__main__":
    # โหลดรายชื่อหุ้น Top 5 จากโปรเจกต์ก่อนหน้า
    top_stocks = ["ADBE", "XOM", "DIS", "CRM", "ABT"]
    
    result = run_fama_french_analysis(top_stocks)
    
    print("\n" + "="*50)
    print("📊 FAMA-FRENCH 3-FACTOR ANALYSIS RESULTS")
    print("="*50)
    print(result.summary())