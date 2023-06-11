# %%
import pandas as pd
import matplotlib.pyplot as plt


# %%


# read data from csv to data frame
FILE_PATH = "data_05_06_2023.csv"
df = pd.read_csv(FILE_PATH)

# %%
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

# %%
# price mean by days to flight

priceMeanByDate = df.groupby("DaysToFlight").mean("Price")
print(priceMeanByDate["Price"])

# chart
plt.plot(priceMeanByDate["Price"])
plt.title("Wykres średnich cen zależny od dni do wylotu")
plt.xlabel("Dni do wylotu")
plt.ylabel("Cena")
plt.show()

# %%
# price mean by month
df["DepartureDate"] = pd.to_datetime(df["DepartureDate"])
priceMeanByMonth = df.groupby(pd.Grouper(key = "DepartureDate", freq = "M")).mean("Price")
priceMeanByMonth.index = priceMeanByMonth.index.strftime("%B")
print(priceMeanByMonth)

# chart
plt.bar(priceMeanByMonth.index, priceMeanByMonth["Price"])

plt.title("Wykres średnich cen zależny od miesiąca")
plt.xlabel("Miesiąc")
plt.ylabel("Średnia cena")
plt.show()

# %%
# most frequent operator from 200 cheapest flights
cheapestFlights = df.sort_values("Price").head(200)
cheapestFlightsDepartureOperator = cheapestFlights["DepartureOperator"].value_counts()
cheapestFlightsReturnOperator = cheapestFlights["ReturnOperator"].value_counts()
operatorsSum = cheapestFlightsDepartureOperator.add(cheapestFlightsReturnOperator, fill_value = 0)

plt.bar(operatorsSum.index, operatorsSum)
plt.title("Wykres operatorów pojawiających się w 200 najtańszych lotach")
plt.xlabel("Operator")
plt.ylabel("Liczba")
plt.show()