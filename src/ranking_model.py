import pandas as pd
import numpy as np
import os  # แก้จุดที่ลืม import

def calculate_scores(df):
    # ใช้ .copy() เพื่อป้องกัน SettingWithCopyWarning
    # และกำจัดค่าว่างออกไปก่อนคำนวณ
    working_df = df.dropna().copy()
    
    # 1. Value Score (P/E, P/B ต่ำ = ดี) 
    # ใช้ .loc เพื่อความปลอดภัยในการเขียนข้อมูล
    working_df.loc[:, 'Value_Score'] = (working_df['PE_Ratio'].rank(ascending=False) + 
                                       working_df['PB_Ratio'].rank(ascending=False)) / 2
    
    # 2. Quality Score (ROE สูง = ดี, D/E ต่ำ = ดี)
    working_df.loc[:, 'Quality_Score'] = (working_df['ROE'].rank(ascending=True) + 
                                         working_df['Debt_to_Equity'].rank(ascending=False)) / 2
    
    # 3. Total Score
    working_df.loc[:, 'Total_Score'] = (working_df['Value_Score'] + working_df['Quality_Score']) / 2
    
    return working_df.sort_values('Total_Score', ascending=False)

if __name__ == "__main__":
    file_path = 'data/raw/us_fundamentals.csv'
    if not os.path.exists(file_path):
        print("❌ ไม่พบไฟล์! กรุณารัน src/data_fetcher.py ก่อน")
    else:
        df = pd.read_csv(file_path, index_col='Ticker')
        ranked_df = calculate_scores(df)
        
        os.makedirs('data/processed', exist_ok=True)
        ranked_df.to_csv('data/processed/us_ranked_stocks.csv')
        
        print("\n🏆 Top 5 'Good & Cheap' Stocks in US Market:")
        print("-" * 50)
        # แสดงผลลัพธ์ที่สำคัญ
        print(ranked_df[['Total_Score', 'PE_Ratio', 'ROE', 'Debt_to_Equity']].head())