import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.interpolate import CubicSpline

# Function to generate random speed for a given hour
def generate_random_speed(hour):
    if 6 <= hour < 9:  # Morning rush hour (slow-moving traffic)
        return random.randint(10, 30)
    elif 9 <= hour < 16:  # Daytime (moderate speed)
        return random.randint(40, 60)
    elif 16 <= hour < 19:  # Evening rush hour (slow-moving traffic)
        return random.randint(10, 30)
    else:  # Nighttime (faster speed)
        return random.randint(70, 100)

# Generate synthetic data for three days
start_date = datetime(2023, 7, 30, 6, 0)  # Start at 6:00 AM
end_date = datetime(2023, 8, 1, 5, 59)  # End at 5:59 AM
time_interval = timedelta(hours=1)  # Data for every hour

data = []
current_date = start_date

while current_date <= end_date:
    speed = generate_random_speed(current_date.hour)
    data.append({
        "Timestamp": current_date,
        "Road Speed": speed,
    })
    current_date += time_interval

# Create a DataFrame from the generated data
df = pd.DataFrame(data)

# Sort the DataFrame by Timestamp
df = df.sort_values(by="Timestamp")

# Convert Timestamp to numeric values (for interpolation)
timestamps_numeric = df["Timestamp"].astype(np.int64)

# Perform cubic spline interpolation
cs = CubicSpline(timestamps_numeric, df["Road Speed"])

# Generate timestamps for smooth curve (more data points for smoothness)
timestamps_smooth = np.linspace(timestamps_numeric.min(), timestamps_numeric.max(), num=1000)

# Get interpolated road speed values
road_speed_smooth = cs(timestamps_smooth)

# Convert interpolated timestamps back to datetime format
timestamps_smooth_datetime = pd.to_datetime(timestamps_smooth)

# Plot the graph with smooth curve
plt.figure(figsize=(12, 6))
plt.plot(timestamps_smooth_datetime, road_speed_smooth, label="Smooth Road Speed", color="blue")
plt.scatter(df["Timestamp"], df["Road Speed"], marker="o", color="red", label="Data Points")
plt.xlabel("Time of Day")
plt.ylabel("Road Speed (km/h)")
plt.title("Average Road Speed During the Day (Smoothed)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
