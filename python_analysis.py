# Importing python librairies needed for the analysis 
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression 
from sklearn.model_selection import train_test_split

# load data
temperature = pd.read_excel("temperature_gaz_dataset.xlsx", sheet_name="temperature", dtype={'date_date': int})
co2 = pd.read_excel("temperature_gaz_dataset.xlsx", sheet_name="co2", dtype={'date_date': int})
ch4 = pd.read_excel("temperature_gaz_dataset.xlsx", sheet_name="ch4", dtype={'date_date': int})
no2 = pd.read_excel("temperature_gaz_dataset.xlsx", sheet_name="no2", dtype={'date_date': int})

#defining common date range
min_date_date = temperature['date_date'].min() , co2['date_date'].min(),ch4['date_date'].min(),no2['date_date'].min()
max_date_date = temperature['date_date'].max() , co2['date_date'].max(),ch4['date_date'].max(),no2['date_date'].max()

min(max_date_date)
max(min_date_date)

#Creating new dataframe to merge the other ones on the right date column
df_all = pd.DataFrame({'date_date': list(range(max(min_date_date),min(max_date_date),))})

#merging on date_date
df_all = df_all.merge(temperature, how="left", on="date_date")
df_all = df_all.merge(co2, how="left", on="date_date")
df_all = df_all.merge(ch4, how="left", on="date_date")
df_all = df_all.merge(no2, how="left", on="date_date")
df_all

#filling null values with previous year values 
df_all = df_all.interpolate(method="backfill")

#Filtering on last 150 years
df_all_last_150 = df_all.tail(150)

#understand the correlation between the features 
matrix_short_term = df_all_last_150[["temperature", "co2", "ch4", "no2"]].corr()
print(matrix_short_term)

#understand temperature's evolution on last 150 years with a plotly express line chart
px.line(df_all_last_150,
        x='date_date',
        y='temperature')
## > it has increased drastically 

#performing linear regression to betetr understand features and correlation on this timeframe

X = df_all_last_150[["co2","ch4","no2"]] 
y = df_all_last_150[["temperature"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

reg = LinearRegression().fit(X_train, y_train)
reg.score(X_test, y_test)

## Data on 150 years seems too correlated, we need to perform a long term analysis on the global dataframe
matrix_long_terme = df_all[["temperature", "co2", "ch4", "no2"]].corr()
print(matrix_long_terme)


#sampling data on larger scale
df_all_50 = df_all[df_all.date_date % 50 == 0]

#Understand tempertature evolution on a larger scale 
px.line(df_all_50,
        x='date_date',
        y='temperature')
#We see a cyclical pattern with different glacial and interglacial patterns. 




