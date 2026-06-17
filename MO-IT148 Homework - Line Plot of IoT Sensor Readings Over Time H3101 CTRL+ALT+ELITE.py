import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("cleaned_zip_blockchain_records.csv")
df["source_timestamp"] = pd.to_datetime(df["source_timestamp"], errors="coerce")

sensors = {
    "temperature_c": "Temperature (C)",
    "humidity_percent": "Humidity (%)",
    "shock_g_force": "Shock (g)",
    "battery_percent": "Battery (%)",
    "speed_kmh": "Speed (km/h)",
    "fuel_percent": "Fuel (%)",
}

for col in sensors:
    df[col] = pd.to_numeric(df[col], errors="coerce")

time_series = (
    df.set_index("source_timestamp")
    .resample("30min")[list(sensors.keys())]
    .mean()
    .dropna(how="all")
)

normalized = (time_series - time_series.min()) / (time_series.max() - time_series.min()) * 100

plt.figure(figsize=(12, 6))
for col, label in sensors.items():
    plt.plot(normalized.index, normalized[col], marker="o", linewidth=2, label=label)

plt.title("IoT Sensor Readings Over Time")
plt.xlabel("Time")
plt.ylabel("Normalized Sensor Value (0-100)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("week7_multisensor_line_plot.png", dpi=160)
plt.show()

print(time_series)
