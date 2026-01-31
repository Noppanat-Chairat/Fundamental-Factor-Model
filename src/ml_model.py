import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
import os

# 1. รวมรายชื่อหุ้นให้เป็นชุดใหญ่ชุดเดียว (ใส่เพิ่มได้ตามใจชอบเลยครับ)
all_tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "AVGO", "ADBE", "CRM",
    "JPM", "V", "MA", "BAC", "WMT", "COST", "PG", "KO", "PEP", "JNJ",
    "PFE", "ABT", "XOM", "CVX", "UNH", "HD", "DIS", "NFLX", "INTC", "AMD",
    "PFE", "CSCO", "ORCL", "GE", "UNP", "IBM", "CAT", "GS", "HON", "BA"
]
def prepare_real_data(tickers):
    print(f"📥 Fetching training data for {len(tickers)} stocks...")
    # 1. โหลดข้อมูล Fundamental ที่เราทำไว้
    fund = pd.read_csv('data/processed/us_ranked_stocks.csv', index_col='Ticker')
    
    # 2. ดึงราคาเพื่อดูว่าเดือนที่ผ่านมาหุ้นขึ้นหรือลง (Target)
    prices = yf.download(list(fund.index), period="2mo")['Close']
    monthly_return = prices.pct_change().iloc[-1]
    
    # สร้าง Target: 1 ถ้ากำไรเป็นบวก, 0 ถ้าติดลบหรือเท่าเดิม
    fund['Target'] = (monthly_return > 0).astype(int)
    
    X = fund[['ROE', 'PE_Ratio', 'Debt_to_Equity']]
    y = fund['Target']
    return X, y

if __name__ == "__main__":
    # 2. ปรับใน main ให้ส่ง all_tickers เข้าไปฝึก AI
    X, y = prepare_real_data(all_tickers)
    
    # กรองข้อมูลที่อาจจะมีค่าว่าง (NaN) ออกก่อนฝึกเพื่อป้องกัน Error
    X = X.dropna()
    y = y.loc[X.index]
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y) # AI เริ่มเรียนรู้จากหุ้น 40 คันนี้
    print(f"\n✅ AI System Ready & Trained on {len(X)} stocks!")

    # --- ขั้นตอน Interactive Search ---
    while True:
        symbol = input("\n🔍 Enter Ticker (e.g., NVDA, TSLA) or 'exit': ").upper()
        if symbol == 'EXIT': break
        
        try:
            ticker_obj = yf.Ticker(symbol)
            info = ticker_obj.info
            
            # ดึงข้อมูลหุ้นที่ User ระบุแบบ Real-time
            input_data = pd.DataFrame([{
                'ROE': info.get('returnOnEquity'),
                'PE_Ratio': info.get('forwardPE'),
                'Debt_to_Equity': info.get('debtToEquity')
            }])
            
            # ทำนายผลและความมั่นใจ
            pred = model.predict(input_data)[0]
            prob = model.predict_proba(input_data)[0]
            
            status = "🚀 POSITIVE (Likely Up)" if pred == 1 else "⚖️ NEUTRAL/DOWN"
            confidence = prob[pred] * 100
            
            print(f"\n--- Analysis for {symbol} ---")
            print(f"🤖 AI Prediction: {status}")
            print(f"🎯 Confidence: {confidence:.2f}%")
            print(f"📊 Stats: ROE: {info.get('returnOnEquity')}, P/E: {info.get('forwardPE')}")
            
        except Exception as e:
            print(f"❌ Could not analyze {symbol}: {e}")