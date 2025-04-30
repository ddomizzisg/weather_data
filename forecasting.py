import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import argparse

def forecast_station_temperature(csv_path, station_id, days=30, output_prefix="forecast"):
    # Load and clean
    df = pd.read_csv(csv_path)
    df['DATE'] = pd.to_datetime(df['DATE'])
    print("type of station_id", type(station_id))
    print("type of df['STATION']", type(df['STATION'][0]))
    df = df[df['STATION'] == station_id]

    if df.empty:
        print(f"No data found for station {station_id}")
        return

    df = df[['DATE', 'TEMP']].replace(9999.9, pd.NA).dropna()
    df['TEMP'] = pd.to_numeric(df['TEMP'], errors='coerce').dropna()
    df['TEMP'] = (df['TEMP'] - 32) * 5 / 9  # Fahrenheit to Celsius
    df = df.rename(columns={"DATE": "ds", "TEMP": "y"})

    # Fit model
    model = Prophet()
    model.fit(df)

    # Forecast
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)

    # Plot and save
    fig = model.plot(forecast)
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

    forecast_station_temperature(args.csv, args.station, days=args.days, output_prefix=args.output_prefix)
