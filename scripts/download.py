# !pip install arch yfinance pandas numpy matplotlib tqdm pyarrow

import os
import time
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import yfinance as yf
from tqdm import tqdm



# ---------------- CONFIG ----------------
tickers = [
"BAJFINANCE.NS","BAJAJFINSV.NS","TITAN.NS","TATASTEEL.NS","JSWSTEEL.NS","M&M.NS",
"SBIN.NS","ADANIENT.NS","AXISBANK.NS","IOC.NS","INDUSINDBK.NS","RELIANCE.NS",
"HDFCBANK.NS","ICICIBANK.NS","LT.NS","EICHERMOT.NS","TATAMOTORS.NS","BPCL.NS",
"UPL.NS","MARUTI.NS","VEDL.NS","TCS.NS","HINDUNILVR.NS","ITC.NS","ADANIPORTS.NS",
"HINDALCO.NS","ZEEL.NS","BAJAJ-AUTO.NS","ONGC.NS","HCLTECH.NS","KOTAKBANK.NS",
"TECHM.NS","GAIL.NS","WIPRO.NS","SHREECEM.NS","COALINDIA.NS","GRASIM.NS",
"INFY.NS","POWERGRID.NS","BRITANNIA.NS","HEROMOTOCO.NS","ASIANPAINT.NS",
"NTPC.NS","NESTLEIND.NS","BHARTIARTL.NS","SUNPHARMA.NS","ULTRACEMCO.NS",
"BEL.NS","CIPLA.NS","DRREDDY.NS"
]

start_date = "2015-01-01"
end_date   = "2025-11-30"
output_dir = "nifty50_history_with_adj"
per_ticker_dir = os.path.join(output_dir, "per_ticker_csvs")
combined_csv_path = os.path.join(output_dir, "nifty50_combined_2015_2025.csv")

sleep_seconds = 0.5   # polite delay between tickers
# ----------------------------------------

os.makedirs(per_ticker_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

def safe_filename(t):
    return t.replace(".","_").replace("/","_").replace(":", "_")

combined_rows = []
missing_adj_tickers = []

# We'll iterate in the order provided so combined CSV has blocks in that order.
for ticker in tqdm(tickers, desc="Tickers"):
    try:
        # Use yf.Ticker.history which typically returns columns:
        # Index Date, Open, High, Low, Close, Volume, Dividends, Stock Splits, Adj Close
        tk = yf.Ticker(ticker)
        df = tk.history(start=start_date, end=end_date, auto_adjust=False)  # keep both Close and Adj Close
        # Alternative: yf.download(ticker, start=start_date, end=end_date)

        if df is None or df.empty:
            print(f"Warning: {ticker} returned no data. Skipping.")
            continue

        # Ensure expected column names and index
        df = df.copy()
        if isinstance(df.index, pd.DatetimeIndex):
            df.index.name = "Date"
        else:
            # Convert index to datetime if needed
            df.index = pd.to_datetime(df.index)
            df.index.name = "Date"

        # Columns that we want in final CSV
        cols_required = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]

        # If 'Adj Close' missing, attempt to get it. yfinance normally supplies it;
        # fallback: set Adj Close = Close and record ticker for user to inspect.
        if "Adj Close" not in df.columns:
            df["Adj Close"] = df["Close"]
            missing_adj_tickers.append(ticker)
            print(f"Note: 'Adj Close' missing for {ticker}. Filled with Close as fallback.")

        # Keep only relevant columns plus Ticker and Date
        df_out = df[["Open", "High", "Low", "Close", "Adj Close", "Volume"]].copy()
        df_out.reset_index(inplace=True)
        df_out["Ticker"] = ticker

        # Save per-ticker CSV (filename safe)
        per_file = os.path.join(per_ticker_dir, f"{safe_filename(ticker)}.csv")
        df_out.to_csv(per_file, index=False)

        # Append to combined rows list (keeps ticker block order)
        combined_rows.append(df_out)

    except Exception as e:
        print(f"Error for {ticker}: {e}")
    time.sleep(sleep_seconds)

# Concatenate all DataFrames in the order appended
if combined_rows:
    combined_df = pd.concat(combined_rows, ignore_index=True, sort=False)
    # Optional: ensure column order
    col_order = ["Date","Ticker","Open","High","Low","Close","Adj Close","Volume"]
    cols_present = [c for c in col_order if c in combined_df.columns]
    combined_df = combined_df[cols_present]
    # Save combined CSV
    combined_df.to_csv(combined_csv_path, index=False)
    print(f"\nCombined CSV written to: {combined_csv_path}")
    print(f"Per-ticker CSVs saved in: {per_ticker_dir}")
    if missing_adj_tickers:
        print("\nTickers where 'Adj Close' was missing and filled with 'Close':")
        print(missing_adj_tickers)
else:
    print("No data downloaded. Check tickers and network connectivity.")
