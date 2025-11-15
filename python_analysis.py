# Earth temperature change analysis
# --------------------------------

import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 1. Load data
file_path = "temperature_gaz_dataset.xlsx"

temperature = pd.read_excel(file_path, sheet_name="temperature", dtype={'date_date': int})
co2 = pd.read_excel(file_path, sheet_name="co2", dtype={'date_date': int})
ch4 = pd.read_excel(file_path, sheet_name="ch4", dtype={'date_date': int})
no2 = pd.read_excel(file_path, sheet_name="no2", dtype={'date_date': int})

# 2. Define common date range (intersection of all datasets)
min_year = max(
    temperature['date_date'].min(),
    co2['date_date'].min(),
    ch4['date_date'].min(),
    no2['date_date'].min()
)

max_year = min(
    temperature['date_date'].max(),
    co2['date_date'].max(),
    ch4['date_date'].max(),
    no2['date_date'].max()
)

# 3. Create base dataframe with full date range
df_all = pd.DataFrame({'date_date': list(range(min_year, max_year + 1))})

# 4. Merge all series on date_date
df_all = df_all.merge(temperature, how="left", on="date_date")
df_all = df_all.merge(co2, how="left", on="date_date")
df_all = df_all.merge(ch4, how="left", on="date_date")
df_all = df_all.merge(no2, how="left", on="date_date")

# 5. Fill missing values (interpolation)
df_all = df_all.interpolate(method="backfill")

# 6. Short-term analysis (last 150 years)
df_all_last_150 = df_all.tail(150)

print("Correlation matrix (last 150 years):")
matrix_short_term = df_all_last_150[["temperature", "co2", "ch4", "no2"]].corr()
print(matrix_short_term)

fig = px.line(
    df_all_last_150,
    x='date_date',
    y='temperature',
    title="Global temperature over the last 150 years"
)
fig.show()

# 7. Linear regression (short-term)
X = df_all_last_150[["co2", "ch4", "no2"]]
y = df_all_last_150[["temperature"]]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

reg = LinearRegression().fit(X_train, y_train)
score = reg.score(X_test, y_test)
print(score)

# 8. Long-term analysis (full dataset)
print("Correlation matrix (full time range):")
matrix_long_term = df_all[["temperature", "co2", "ch4", "no2"]].corr()
print(matrix_long_term)

# Sample every 50 years for long-term visualisation
df_all_50 = df_all[df_all["date_date"] % 50 == 0]

fig2 = px.line(
    df_all_50,
    x='date_date',
    y='temperature',
    title="Global temperature over the last 800,000 years (sampled every 50 years)"
)
fig2.show()
 




