import yfinance as yf
import pandas as pd
import os

def fetch_fundamental_data(tickers):
    fund_data = []
    print(f"🚀 Fetching fundamentals for: {tickers}")
    
    for t in tickers:
        try:
            ticker = yf.Ticker(t)
            info = ticker.info
            
            # ดึงค่าที่ต้องการ (Value & Quality)
            fund_data.append({
                'Ticker': t,
                'Price': info.get('currentPrice'),
                'PE_Ratio': info.get('forwardPE'),          # Value: ต่ำ = ถูก
                'PB_Ratio': info.get('priceToBook'),         # Value: ต่ำ = ถูก
                'ROE': info.get('returnOnEquity'),          # Quality: สูง = เก่ง
                'Debt_to_Equity': info.get('debtToEquity'), # Quality: ต่ำ = ปลอดภัย
                'MarketCap': info.get('marketCap')
            })
            print(f"✅ {t} fetched")
        except Exception as e:
            print(f"⚠️ {t} skipped: {e}")
            
    df = pd.DataFrame(fund_data).set_index('Ticker')
    return df

if __name__ == "__main__":
    # หุ้นบิ๊กเนมสหรัฐฯ (Dow Jones 30)
    us_tickers = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "V", "JPM", "JNJ", "WMT",
        "PG", "HD", "MA", "UNH", "DIS", "BAC", "PFE", "KO", "PEP", "XOM",
        "CVX", "COST", "AVGO", "ADBE", "CRM", "NKE", "NFLX", "TMO", "CSCO", "ABT"
    ]
    
    df_fundamentals = fetch_fundamental_data(us_tickers)
    
    os.makedirs('data/raw', exist_ok=True)
    df_fundamentals.to_csv('data/raw/us_fundamentals.csv')
    print("\n💾 Saved fundamental data to data/raw/us_fundamentals.csv")