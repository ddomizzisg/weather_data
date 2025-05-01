import pandas as pd
import glob
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
from sklearn.linear_model import LinearRegression  

class StationsLinearRegression:

    def __init__(self, df, year_col, temp_col):
        self.df = df
        self.year_col = year_col
        self.temp_col = temp_col

    def fit(self):


        x = self.df[self.year_col].values.reshape(-1, 1)
        y = self.df[self.temp_col].values

        # Fit the linear regression model
        model = LinearRegression()
        model.fit(x, y)
        self.slope = model.coef_[0]
        self.intercept = model.intercept_
        self.r_squared = model.score(x, y)
        return self.slope, self.intercept, self.r_squared
    
    def predict(self, year):
        return self.intercept + self.slope * year
    
    def plot(self, output="regression.png"):
        plt.figure(figsize=(10, 6))
        plt.scatter(self.df[self.year_col], self.df[self.temp_col], color='blue', label='Data Points')
        plt.plot(self.df[self.year_col], self.predict(self.df[self.year_col]), color='red', label='Regression Line')
        plt.title('Average Temperature per Year with Regression Line')
        plt.xlabel('Year')
        plt.ylabel('Average Temperature')
        plt.legend()
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

    # Reads the CSV file
    df = pd.read_csv(args.csv_path)

    if args.state_code is not None and args.state_code != 0:
        # Filter the dataframe for the specified state
        df = df[df['STATE_CODE'] == args.state_code]

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

    #print(avg_temp_per_year)

    regression = StationsLinearRegression(avg_temp_per_year, 'YEAR', 'TEMP')
    regression.fit()
    regression.plot(args.output)
    print(f"Regression plot saved to {args.output}")