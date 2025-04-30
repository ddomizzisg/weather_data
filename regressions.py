import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

def get_regressions(csv_path, state=None, output="regression.png", dataset="data"):

    print(state)
    # Path to your CSV files (adjust the pattern as needed)
    df = pd.read_csv(csv_path)
    
    if state is not None and state != 0:
        # Filter the dataframe for the specified state
        df = df[df['STATE_CODE'] == state]

    print(df)

    # Ensure 'DATE' is datetime
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')

    # Extract year and convert temperature to numeric
    df['YEAR'] = df['DATE'].dt.year
    df['TEMP'] = pd.to_numeric(df['TEMP'], errors='coerce')

    # Convert from Fahrenheit to Celsius
    df['TEMP'] = (df['TEMP'] - 32) * 5 / 9

    # Drop rows with missing years or temperatures
    df = df.dropna(subset=['YEAR', 'TEMP'])

    # Group by year and compute average temperature
    avg_temp_per_year = df.groupby('YEAR')['TEMP'].mean().reset_index()

    # Remove year 2025
    avg_temp_per_year = avg_temp_per_year[avg_temp_per_year['YEAR'] != 2025]

    # Plot regression
    sns.set(style='whitegrid')
    plt.figure(figsize=(10, 6))
    sns.regplot(data=avg_temp_per_year, x='YEAR', y='TEMP', marker='o', line_kws={"color": "red"})
    plt.title('Average Temperature per Year with Regression Line')
    plt.xlabel('Year')
    plt.ylabel('Average Temperature')
    plt.tight_layout()
    plt.savefig(output)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot average temperature per year with regression.")
    parser.add_argument("csv_path", type=str, help="Path to the CSV file.")
    parser.add_argument("--state-code", type=int, default=0, help="State to filter data (optional).")
    parser.add_argument("--output", type=str, default="regression.png", help="Output filename for the plot.")
    parser.add_argument("--dataset", type=str, default="data", help="Directory containing the CSV files.")
    args = parser.parse_args()


    get_regressions(args.csv_path, state=args.state_code, output=args.output, dataset=args.dataset)