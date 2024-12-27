import os
import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna

# Directory paths
RAW_DATA_DIR = "data"
PROCESSED_DATA_DIR = "processed_data"

def preprocess_data(asset_type: str):
    """
    Preprocess data for a given asset type.
    Args:
        asset_type (str): The type of asset (e.g., 'stocks', 'etfs', etc.).
    """
    input_dir = os.path.join(RAW_DATA_DIR, asset_type)
    output_dir = os.path.join(PROCESSED_DATA_DIR, asset_type)
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        try:
            print(f"Processing {filename}...")
            df = pd.read_csv(filepath)

            # Ensure 'timestamp' column is datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)

            # Drop rows with missing values
            df = dropna(df)

            # Add technical indicators (RSI, MACD, Bollinger Bands, etc.)
            df = add_all_ta_features(
                df, open="Open", high="High", low="Low", close="close_price", volume="Volume", fillna=True
            )

            # Save preprocessed data
            output_path = os.path.join(output_dir, filename)
            df.reset_index(inplace=True)
            df.to_csv(output_path, index=False)
            print(f"Saved preprocessed data to {output_path}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

def main():
    for asset_type in os.listdir(RAW_DATA_DIR):
        asset_path = os.path.join(RAW_DATA_DIR, asset_type)
        if os.path.isdir(asset_path):
            print(f"Preprocessing data for {asset_type}...")
            preprocess_data(asset_type)
    print("Data preprocessing complete.")

if __name__ == "__main__":
    main()
