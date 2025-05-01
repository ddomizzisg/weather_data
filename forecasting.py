import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import argparse

class WeatherForecast:

    def __init__(self, df):
        self.df = df

    def fit(self, station_id, column_station_name, date_column, temp_column):
        print(self.df.columns)
        self.df_station = self.df[self.df[column_station_name] == station_id]
        self.df_station = self.df_station.reset_index(drop=True)

        if self.df_station.empty:
            print(f"No data found for station {station_id}")
            return
        
        self.df_station[date_column] = pd.to_datetime(self.df_station[date_column])
        self.df_station = self.df_station[[date_column, temp_column]].replace(9999.9, pd.NA).dropna()
        self.df_station[temp_column] = pd.to_numeric(self.df_station[temp_column], errors='coerce').dropna()
        self.df_station[temp_column] = (self.df_station[temp_column] - 32) * 5 / 9
        self.df_station = self.df_station.rename(columns={date_column: "ds", temp_column: "y"})

        # Fit model
        self.model = Prophet()
        self.model.fit(self.df_station)

    def forecast(self, days=30):
        future = self.model.make_future_dataframe(periods=days)
        forecast = self.model.predict(future)
        return forecast
    
    def plot(self, forecast, station_id, output_prefix="forecast"):
        fig = self.model.plot(forecast)
        plt.title(f"Temperature Forecast - Station {station_id}")
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.tight_layout()
        plot_path = f"{output_prefix}_{station_id}.png"
        csv_path = f"{output_prefix}_{station_id}.csv"
        plt.savefig(plot_path)
        plt.close()

        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(csv_path, index=False)
        print(f"Forecast saved to {plot_path} and {csv_path}")



# CLI entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Forecast temperature for a specific station.")
    parser.add_argument("csv", help="Path to the CSV file with weather data.")
    parser.add_argument("station", type=int, help="Station number (string).")
    parser.add_argument("--days", type=int, default=30, help="Number of future days to predict.")
    parser.add_argument("--output-prefix", default="forecast", help="Prefix for output files.")
    args = parser.parse_args()

    # Load data
    df = pd.read_csv(args.csv)

    # Initialize and fit the model
    wf = WeatherForecast(df)

    wf.fit(args.station, column_station_name="STATION", date_column="DATE", temp_column="TEMP")
    forecast = wf.forecast(days=args.days)
    wf.plot(forecast, args.station, output_prefix=args.output_prefix)
    print(f"Forecast for station {args.station} saved to {args.output_prefix}_{args.station}.png and {args.output_prefix}_{args.station}.csv")
