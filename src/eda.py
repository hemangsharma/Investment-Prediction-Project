import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Directory for preprocessed data
PROCESSED_DATA_DIR = "processed_data"
EDA_OUTPUT_DIR = "eda_plots"

# Create output directory for EDA plots
os.makedirs(EDA_OUTPUT_DIR, exist_ok=True)

def plot_time_series(df, filename, column, asset_type):
    """
    Plot a time series for a specific column.
    Args:
        df (pd.DataFrame): DataFrame containing the data.
        filename (str): Name of the file.
        column (str): Column to plot.
        asset_type (str): Type of asset for subfolder organization.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df[column], label=column, color='blue')
    plt.title(f"{column} over Time - {filename}")
    plt.xlabel("Date")
    plt.ylabel(column)
    plt.legend()
    plt.grid(True)

    # Save the plot
    asset_dir = os.path.join(EDA_OUTPUT_DIR, asset_type)
    os.makedirs(asset_dir, exist_ok=True)
    plot_path = os.path.join(asset_dir, f"{filename}_{column}.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"Saved plot: {plot_path}")

def eda_for_asset(asset_type: str):
    """
    Perform EDA for a specific asset type.
    Args:
        asset_type (str): The type of asset (e.g., 'stocks', 'etfs', etc.).
    """
    input_dir = os.path.join(PROCESSED_DATA_DIR, asset_type)
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        try:
            print(f"Performing EDA for {filename}...")
            df = pd.read_csv(filepath)

            # Ensure 'timestamp' column is datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])

            # Descriptive statistics
            stats = df.describe()
            print(f"Descriptive Statistics for {filename}:\n{stats}")

            # Correlation heatmap
            corr = df.corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
            plt.title(f"Correlation Heatmap - {filename}")
            heatmap_path = os.path.join(EDA_OUTPUT_DIR, asset_type, f"{filename}_heatmap.png")
            os.makedirs(os.path.dirname(heatmap_path), exist_ok=True)
            plt.savefig(heatmap_path)
            plt.close()
            print(f"Saved heatmap: {heatmap_path}")

            # Time-series plots for key columns
            for column in ['close_price', 'volume', 'momentum_rsi', 'trend_macd']:
                if column in df.columns:
                    plot_time_series(df, filename, column, asset_type)
        except Exception as e:
            print(f"Error in EDA for {filename}: {e}")

def main():
    for asset_type in os.listdir(PROCESSED_DATA_DIR):
        asset_path = os.path.join(PROCESSED_DATA_DIR, asset_type)
        if os.path.isdir(asset_path):
            print(f"Starting EDA for {asset_type}...")
            eda_for_asset(asset_type)
    print("EDA completed.")

if __name__ == "__main__":
    main()