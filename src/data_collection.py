import yfinance as yf
import pandas as pd
import os

# Define a list of assets with their Yahoo Finance tickers
ASSETS = {
    "stocks": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
    "etfs": ["SPY", "VOO", "QQQ", "VTI"],
    "commodities": ["GC=F", "CL=F", "SI=F", "HG=F"],  # Gold, Crude Oil, Silver, Copper
    "currencies": ["EURUSD=X", "JPY=X", "GBPUSD=X", "AUDUSD=X"],  # Currency pairs
}

# Base directory for saving data
DATA_DIR = "data"

def fetch_and_save_data(asset_type: str, symbols: list):
    """
    Fetch and save historical data for a given list of symbols.
    Args:
        asset_type (str): Type of asset (e.g., 'stocks', 'etfs', 'commodities', 'currencies').
        symbols (list): List of ticker symbols for the asset type.
    """
    # Create directory for the asset type if it doesn't exist
    asset_dir = os.path.join(DATA_DIR, asset_type)
    os.makedirs(asset_dir, exist_ok=True)
    
    for symbol in symbols:
        try:
            print(f"Fetching data for {symbol}...")
            # Fetch historical data
            data = yf.download(symbol, start="2010-01-01")
            if data.empty:
                print(f"No data found for {symbol}")
                continue

            # Reset index and save to CSV
            data.reset_index(inplace=True)
            data.rename(columns={"Date": "timestamp", "Close": "close_price"}, inplace=True)
            filepath = os.path.join(asset_dir, f"{symbol}.csv")
            data.to_csv(filepath, index=False)
            print(f"Data for {symbol} saved to {filepath}")
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

def main():
    for asset_type, symbols in ASSETS.items():
        print(f"Fetching data for {asset_type}...")
        fetch_and_save_data(asset_type, symbols)
    print("Data collection complete.")

if __name__ == "__main__":
    main()