from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
import calendar

departureDate = ["2023-06-29",  "2023-07-29", "2023-07-29"]
returnDate = ["2023-07-06", "2023-08-29", "2023-09-29"]

priceList = []
departureOperatorList = []
returnOperatorList = []
departureDateList = []
returnDateList = []


for i in range(len(departureDate)):
  driver = webdriver.Chrome()

  url = "https://www.kayak.pl/flights/KRK-ROM/{departureDate}/{returnDate}-flexible-2days?sort=bestflight_a".format(
      departureDate=departureDate[i], 
      returnDate=returnDate[i]
   )
  
  driver.get(url)
  
  cookiesPopupAcceptXPath = '//button[@class = "Iqt3 Iqt3-mod-stretch Iqt3-mod-bold Button-No-Standard-Style Iqt3-mod-variant-outline Iqt3-mod-theme-base Iqt3-mod-shape-rounded-small Iqt3-mod-shape-mod-default Iqt3-mod-spacing-default Iqt3-mod-size-small"]'

  WebDriverWait(driver, timeout=20).until(lambda d: d.find_elements(By.XPATH, cookiesPopupAcceptXPath) != [])
  
  driver.find_element(By.XPATH, cookiesPopupAcceptXPath).click()

  # wait for progress bar loading end
  progressBarXPath = '//div[@class = "c3kRN-visually-hidden"]'
  
  WebDriverWait(driver, timeout=20).until(lambda d:  d.find_element(By.XPATH, progressBarXPath).text == "Wyniki gotowe.")

  print("progress bar loaded")


  cardWrapperPath = '//div[@class = "nrc6-wrapper"]'

  fligthtCards = driver.find_elements(By.XPATH, cardWrapperPath)


  for WebElement in fligthtCards:
      elementHTML = WebElement.get_attribute('outerHTML')
      elementSoup = BeautifulSoup(elementHTML, 'html.parser')

      # Prices
      price = elementSoup.find("div", {"class": "f8F1-price-text"}).text
      price = price.split("z")[0]
      try:
        priceList.append(int(price))
      except ValueError:
         pass
      
      # Operators
      operators = elementSoup.find("div", {"class": "J0g6-operator-text"}).text
      try:
         operatorsSplit = operators.split(", ")
      except ValueError:
         pass
      
      print(operatorsSplit)
      
      departureOperatorList.append(operatorsSplit[0])
      try:
         returnOperatorList.append(operatorsSplit[1])
      except IndexError:
         returnOperatorList.append(operatorsSplit[0])  

      departureDateList.append(departureDate[i]) 
      returnDateList.append(returnDate[i])


print(len(priceList), len(departureDateList), len(returnOperatorList))
# Data to data frame
df = pd.DataFrame(
   list(zip(
      priceList, departureOperatorList, returnOperatorList, departureDateList, returnDateList
      )), 
    columns=["Cena", "Operator wylotu", "Operator Przylotu", "Data Wylotu", "Data przylotu"])
print(df)

df.to_csv("./data.csv", index=True)
print("sex")



