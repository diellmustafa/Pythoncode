# 1. Temperature Overview
# -find the average temperature for the  entire dataset (format 2 decimal points)
#
# 2. Monthly Temperature
# -calculate the average temperature for each month, visualize the monthly average temperature -> bar plot
#
# 3. High and Lows
# -Identify the hottest and coldest days based on temperature
#
# 4. Temperature Trends
# -create a simple line graph showing how temperature changes over time
# -season average temperature
#CKBZIK

import pandas as pd
import plotly.express as px

df = pd.read_csv("weather_tokyo_data.csv")

temp = df['temperature'][0].split()
temp = [float(t.replace('(', '').replace(')','')) for t in temp if t.strip()]

avg = sum(temp)/len(temp)
print(avg)

df['day'] = pd.to_datetime(df['day'], format='%m/%d')

# Step 3: Extract the month from the 'day' column
df['month'] = df['day'].dt.month

# Step 4: Calculate the average temperature for each month
monthly_avg_temp = df.groupby('month')['temperature'].mean().reset_index()

# Step 5: Create a bar plot to visualize the average monthly temperature
fig = px.bar(monthly_avg_temp,
             x='month',
             y='temperature',
             title='Average Monthly Temperature in Tokyo',
             labels={'month': 'Month', 'temperature': 'Average Temperature (°C)'},
             color='month',
             color_continuous_scale='Viridis')

# Show the plot
fig.show()