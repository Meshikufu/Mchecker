import plotly.express as px
import pandas as pd
from datetime import datetime
import os

directory = r"C:\Users\Kufu\PythonProjects\Mchecker\gBot"
data_file = os.path.join(directory, "Gdata2023.csv")

with open(data_file, 'r') as file:
    lines = file.readlines()

data = [line.strip().split(',') for line in lines]
dates = []
times = []
price = []
names = []
quantity = []
level = []

for entry in data:
    date_str, time_str, offer_price_str, name_str, quantity_str, level_str = entry
    date_time_str = f"{date_str.strip()} {time_str.strip()}"
    date_time = datetime.strptime(date_time_str, "%d - %m - %Y %H:%M:%S")
    dates.append(date_time)
    price.append(float(offer_price_str.strip()))
    names.append(name_str.strip())
    quantity.append(int(quantity_str.strip()))
    level.append(int(level_str.strip()))

# Create the DataFrame
df = pd.DataFrame({'DateTime': dates, 'Price': price, 'Name': names, 'Stock': quantity, 'lvl': level})

# Create a custom hover template
hover_template = (
    "<b>%{customdata[0]}</b> | "
    "Price: %{y:$,.2f} | "
    "Stock: %{customdata[1]} | "
    "lvl: %{customdata[2]}<extra></extra>"
)

# Create a Plotly figure with custom hover template
fig = px.line(df, x='DateTime', y='Price', color='Name', custom_data=['Name', 'Stock', 'lvl'])
fig.update_traces(mode='lines+markers', hovertemplate=hover_template)
fig.update_layout(yaxis=dict(rangemode='tozero'), hovermode='x')
fig.show()

#fig.update_traces(mode='lines', hovertemplate=hover_template)