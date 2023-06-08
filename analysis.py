import pandas as pd

# read data from csv to data frame
FILE_PATH = "data_05_06_2023.csv"
df = pd.read_csv(FILE_PATH)

# rename data columns
df = df.rename(
    columns={
        "Unnamed: 0": "Id",
        "priceList": "Price",
        "departureOperatorList": "DepartureOperator",
        "returnOperatorList": "ReturnOperator",
        "departureDateList": "DepartureDate",
        "returnDateList": "ReturnDate",
        "daysToFlight": "DaysToFlight",
    }
)

print(df.head())