# Multi-Factor Fundamental Analysis & Asset Pricing Model (US Equities)

This project develops a **Smart Beta Strategy** based on **Value** and **Quality** factors for S&P 500 constituents. It integrates automated financial data retrieval with rigorous statistical verification using the **Fama-French 3-Factor Model**.

## 🎯 Project Objectives
* **Factor Discovery:** Identify "Good and Cheap" stocks by combining Valuation (P/E, P/B) and Quality (ROE, Debt-to-Equity) metrics.
* **Statistical Rigor:** Decompose portfolio returns using OLS Regression to isolate **Alpha** from systematic risk premiums.
* **Data Engineering:** Build a robust pipeline to synchronize disparate data sources (Yahoo Finance & Kenneth French Data Library).

## 🛠️ Tech Stack
* **Language:** Python 3.9+
* **Core Libraries:** * `Pandas` & `NumPy`: Data manipulation and vectorized scoring.
  * `YFinance`: Financial statement and ratio ingestion.
  * `Statsmodels`: Econometric modeling and OLS regression.
  * `Pandas-DataReader`: Remote data access for Fama-French factors.

## 📊 Methodology & Scoring Logic
The model ranks stocks using a composite score:
1. **Value Score:** Inverted ranking of Forward P/E and Price-to-Book ratios.
2. **Quality Score:** Combined ranking of Return on Equity (ROE) and Debt-to-Equity (Inverted).
3. **Selection:** The top 5-10 stocks are selected for the model portfolio.

## 📈 Statistical Results (Fama-French Decomposition)
The portfolio analysis for the 2020-2025 period yielded the following:
* **Market Beta (Mkt-RF):** 1.11 (p < 0.05) – Indicating a slight leverage to the broader market.
* **Value Loading (HML):** Positive coefficient, confirming the successful tilt towards undervalued assets.
* **R-Squared:** 0.765 – Demonstrating that over 76% of portfolio variance is explained by the three factors.

## Conclusion

The model successfully identifies high-quality value stocks. While the current alpha is neutral after accounting for market factors, the systematic exposure (Beta) and Value tilt (HML) align perfectly with the investment thesis, proving the model's structural integrity.

## 📂 Project Structure
```text
├── data/
│   ├── raw/             # Raw fundamental data
│   └── processed/       # Ranked and scored stocks
├── src/
│   ├── data_fetcher.py  # Automated API ingestion
│   ├── ranking_model.py # Composite score logic
│   └── analyzer.py      # Fama-French regression & stats
└── README.md

