import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os
import random
import numpy as np
import matplotlib.patheffects as pe

# Define the directory path
directory = r"C:\Users\Kufu\PythonProjects\Mchecker\gBot"

# Combine the directory path and the data file name
data_file = os.path.join(directory, "Gdata2023.csv")

with open(data_file, 'r') as file:
    lines = file.readlines()

# Convert the data to a format suitable for Pandas DataFrame
data = [line.strip().split(',') for line in lines]
dates = []
times = []
offer_prices = []
names = []
quantity = []

for entry in data:
    date_str, time_str, offer_price_str, name_str, quantity_str = entry
    date_time_str = f"{date_str.strip()} {time_str.strip()}"
    date_time = datetime.strptime(date_time_str, "%d - %m - %Y %H:%M:%S")
    dates.append(date_time)
    offer_prices.append(float(offer_price_str.strip()))
    names.append(name_str.strip())
    quantity.append(int(quantity_str.strip()))

# Create the DataFrame
df = pd.DataFrame({'DateTime': dates, 'Offer_Price': offer_prices, 'Name': names, 'Quantity': quantity})

# Get unique names
unique_names = df['Name'].unique()



# Plot the time series graph
plt.figure(figsize=(10, 6))

# Plot each name with a different color
for name in unique_names:
    name_data = df[df['Name'] == name]
    
    # Generate a random color for the line and dot
    line_color = np.random.rand(3,)  # RGB values between 0 and 1
    plt.plot(name_data['DateTime'], name_data['Offer_Price'], marker='o', label='_nolegend_', color=line_color)
    
    last_index = name_data.index[-1]
    display_quantity = name_data.at[last_index, 'Quantity']
    if display_quantity > 999:
        display_quantity = '999+'
    annotation_text = f"{name} ({display_quantity})"
    
    # Generate a random angle in radians (0 to 2*pi)
    random_angle = random.uniform(0, 2 * np.pi)
    
    # Define the radius for placing the annotation text
    radius = 0.1 * max(df['Offer_Price'])  # Adjust the value to control the distance from the dot
    
    # Calculate the x and y offsets based on the angle and radius
    random_offset_x = radius * np.cos(random_angle)
    random_offset_y = radius * np.sin(random_angle)
    
    # Add outline effect to the annotation text
    path_effects = [pe.withStroke(linewidth=1, foreground='black')]
    
    plt.annotate(annotation_text, (name_data.at[last_index, 'DateTime'], name_data.at[last_index, 'Offer_Price']),
                 textcoords="offset points", xytext=(random_offset_x, random_offset_y), ha='center', color=line_color,
                 path_effects=path_effects)  # Set the path_effects parameter
    
plt.xlabel('Date and Time')
plt.ylabel('Offer Price')
plt.title('Offer Price Time Series')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()