from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import datetime
import re

# specifying date range for scraping
today = datetime.date.today()
endDate = datetime.date(today.year, 12, 31)

# flight data dictionary
data = {
   'priceList': [],
   'departureOperatorList': [],
   'returnOperatorList': [],
   'departureDateList': [],
   'returnDateList': [],
   'daysToFlight': [],
}

currDate = today

while currDate <= endDate:
  # format date to YYYY-DD-MM format
  departureDate = currDate.strftime("%Y-%m-%d")
  returnDate = (currDate + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
  print(returnDate)
  
  driver = webdriver.Chrome()

  url = "https://www.kayak.pl/flights/KRK-ROM/{departureDate}/{returnDate}-flexible-2days?sort=bestflight_a".format(
      departureDate=departureDate, 
      returnDate=returnDate,
   )
  
  driver.get(url)
  sleep(5)
  
  cookiesPopupAcceptXPath = '//button[@class = "Iqt3 Iqt3-mod-stretch Iqt3-mod-bold Button-No-Standard-Style Iqt3-mod-variant-outline Iqt3-mod-theme-base Iqt3-mod-shape-rounded-small Iqt3-mod-shape-mod-default Iqt3-mod-spacing-default Iqt3-mod-size-small"]'

  # wait for cookies popup to appear
  try:
   WebDriverWait(driver, timeout=50).until(lambda d: d.find_elements(By.XPATH, cookiesPopupAcceptXPath) != [])
  except TimeoutException as e:
   print("cookies popup loading timeout")
   print(e)
   driver.quit()
   break
  
  driver.find_element(By.XPATH, cookiesPopupAcceptXPath).click()

  progressBarXPath = '//div[@class = "c3kRN-visually-hidden"]'

  # check if progress bar is on website 
  isProgressBarOnWebsite = driver.find_elements(By.XPATH, progressBarXPath) != []

  # if progress bar is not on website, try again loading site
  if(not isProgressBarOnWebsite):
     print("no progress bar on website")
     continue

  # wait for progress bar loading end if it is on website 
  try:
   WebDriverWait(driver, timeout=50).until(lambda d:  d.find_element(By.XPATH, progressBarXPath).text == "Wyniki gotowe.")
  except TimeoutException as e:
   print("progress bar loading timeout")
   print(e)
   driver.quit()
   break 

  print("progress bar loaded")


  cardWrapperPath = '//div[@class = "nrc6-wrapper"]'

  flightCards = driver.find_elements(By.XPATH, cardWrapperPath)


  for WebElement in flightCards:
      elementHTML = WebElement.get_attribute('outerHTML')
      elementSoup = BeautifulSoup(elementHTML, 'html.parser')

      # Prices
      price = elementSoup.find("div", {"class": "f8F1-price-text"}).text
      price = price.split("z")[0]
      # remove spaces from price
      price = re.sub(r"\s+", '', price)
      print(price)
      try:
        data['priceList'].append(int(price))
      except ValueError:
         print("Price cannot be converted to integer")
         break;
      
      # Operators
      operators = elementSoup.find("div", {"class": "J0g6-operator-text"}).text
      try:
         operatorsSplit = operators.split(", ")
      except ValueError:
         pass
      
      print(operatorsSplit)
      data['departureOperatorList'].append(operatorsSplit[0])
      try:  
         data['returnOperatorList'].append(operatorsSplit[1])
      except IndexError:
         data['returnOperatorList'].append(operatorsSplit[0])  

      data['departureDateList'].append(departureDate) 
      data['returnDateList'].append(returnDate)

      # count and add days to flight
      data['daysToFlight'].append((currDate - today).days)
  currDate += datetime.timedelta(days=1)

driver.quit()

print(data)

# Add data to data frame
df = pd.DataFrame(data)

df.to_csv("./data.csv", index=True)



