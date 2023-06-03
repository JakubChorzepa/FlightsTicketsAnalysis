from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import calendar

departureDate = ["2023-06-29",  "2023-07-29", "2023-07-29"]
returnDate = ["2023-07-06", "2023-08-29", "2023-09-29"]

# data dictionary
data = {
   'priceList': [],
   'departureOperatorList': [],
   'returnOperatorList': [],
   'departureDateList': [],
   'returnDateList': [],
}


for i in range(len(departureDate)):
  print("iteration: ", i)
  driver = webdriver.Chrome()

  url = "https://www.kayak.pl/flights/KRK-ROM/{departureDate}/{returnDate}-flexible-2days?sort=bestflight_a".format(
      departureDate=departureDate[i], 
      returnDate=returnDate[i]
   )
  
  driver.get(url)

  sleep(5)
  
  cookiesPopupAcceptXPath = '//button[@class = "Iqt3 Iqt3-mod-stretch Iqt3-mod-bold Button-No-Standard-Style Iqt3-mod-variant-outline Iqt3-mod-theme-base Iqt3-mod-shape-rounded-small Iqt3-mod-shape-mod-default Iqt3-mod-spacing-default Iqt3-mod-size-small"]'

  WebDriverWait(driver, timeout=30).until(lambda d: d.find_elements(By.XPATH, cookiesPopupAcceptXPath) != [])
  
  driver.find_element(By.XPATH, cookiesPopupAcceptXPath).click()

  progressBarXPath = '//div[@class = "c3kRN-visually-hidden"]'

  # check if progress bar is on website 
  isProgressBarOnWebsite = driver.find_elements(By.XPATH, progressBarXPath) != []

  # wait for progress bar loading end if it is on website
  if(isProgressBarOnWebsite):  
   try:
      WebDriverWait(driver, timeout=20).until(lambda d:  d.find_element(By.XPATH, progressBarXPath).text == "Wyniki gotowe.")
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
      try:
        data['priceList'].append(int(price))
      except ValueError:
         pass
      
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

      data['departureDateList'].append(departureDate[i]) 
      data['returnDateList'].append(returnDate[i])

driver.quit()

# Data to data frame
df = pd.DataFrame(data)
print(df)

df.to_csv("./data.csv", index=True)



