# statistical_analysis.py
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from statsmodels.tsa.seasonal import seasonal_decompose
from hashing_utils import read_csv_file

def perform_statistical_analysis() -> None:

    directory_path = input("Enter the directory path: ").strip()
    file_name = input("Enter the file name (without extension): ").strip()
    extension = input("Enter the file extension: ").strip()
    file_path = os.path.join(directory_path, f"{file_name}.{extension}")

    df = read_csv_file(file_path)

    # Remove rows where 'Disconnection Date' is not a string
    df = df[df['Disconnection Date'].apply(lambda x: isinstance(x, str))]

    df['Disconnection Date'] = pd.to_datetime(df['Disconnection Date'], format='%Y-%m-%d', errors='coerce')

    # Drop rows where 'Disconnection Date' conversion failed
    df.dropna(subset=['Disconnection Date'], inplace=True)

    # Count disconnections by reason
    disconnection_counts = df['Disconnection Reason'].value_counts()
    print(disconnection_counts)

    # Plot disconnection counts by reason
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Disconnection Reason')
    plt.title('Count of Disconnections by Reason')
    plt.xticks(rotation=45)
    plt.show()

    df['Weekday'] = df['Disconnection Date'].dt.day_name()
    df['Month'] = df['Disconnection Date'].dt.month_name()

    # Plot disconnections by weekday
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Weekday', order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    plt.title('Number of Disconnections by Weekday')
    plt.xticks(rotation=45)
    plt.show()

    # Plot disconnections by month
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='Month', order=[month for month in df['Month'].unique()])
    plt.title('Number of Disconnections by Month')
    plt.xticks(rotation=45)
    plt.show()

    # Create  heatmap of disconnections by weekday and month
    heatmap_data = df.pivot_table(index='Weekday', columns='Month', aggfunc='size', fill_value=0)
    heatmap_data = heatmap_data.reindex(index=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlGnBu')
    plt.title('Heatmap of Disconnections by Weekday and Month')
    plt.show()

    # Resample data on a monthly basis
    monthly_data = df.resample('ME', on='Disconnection Date').size()

    plt.figure(figsize=(12, 6))
    monthly_data.plot()
    plt.title('Monthly Disconnections Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Disconnections')
    plt.show()

    # Check if there are enough observations for seasonal decomposition
    if len(monthly_data) >= 24:
        # Time series decomposition
        result = seasonal_decompose(monthly_data, model='additive')

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
        result.observed.plot(ax=ax1, legend=False)
        ax1.set_ylabel('Observed')
        result.trend.plot(ax=ax2, legend=False)
        ax2.set_ylabel('Trend')
        result.seasonal.plot(ax=ax3, legend=False)
        ax3.set_ylabel('Seasonal')
        result.resid.plot(ax=ax4, legend=False)
        ax4.set_ylabel('Residual')
        plt.xlabel('Date')
        plt.suptitle('Time Series Decomposition')
        plt.show()
    else:
        print(f"Not enough data for seasonal decomposition. Requires 24 observations, but only {len(monthly_data)} available.")

    # Plotting moving average
    df.set_index('Disconnection Date', inplace=True)
    moving_avg = df['Disconnection Reason'].resample('ME').count().rolling(window=3).mean()
    moving_avg.plot(figsize=(12, 6))
    plt.title('3-Month Moving Average of Disconnections')
    plt.xlabel('Date')
    plt.ylabel('Number of Disconnections')
    plt.show()

    # Year-over-year comparison
    df['Year'] = df.index.year
    df['Month'] = df.index.month

    pivot_data = df.pivot_table(index='Month', columns='Year', values='Disconnection Reason', aggfunc='size', fill_value=0)

    # Plot year-over-year comparison of monthly disconnections
    pivot_data.plot(figsize=(12, 8))
    plt.title('Year-over-Year Comparison of Monthly Disconnections')
    plt.xlabel('Month')
    plt.ylabel('Number of Disconnections')
    plt.show()
