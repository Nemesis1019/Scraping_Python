from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time


options = webdriver.ChromeOptions()
options.add_argument('--headless') 

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#Acá puedes  modificar la url que quieras analizar
url = "https://www.blush-bar.com/descuentos?gad_source=1&gad_campaignid=17675834857&gbraid=0AAAAADNyDcAM4UoIAjyWe0Fd7qq3SLOM7&gclid=Cj0KCQjwyIPDBhDBARIsAHJyyVjWO9uJ-84dnXQ5VD0dpTROO1Zv1-MvHgS8pzBo0emhuGn_2khSGDQaAnzdEALw_wcB"
driver.get(url)

items = driver.find_elements(By.CSS_SELECTOR, "a.vtex-product-summary-2-x-clearLink") 
linksToProduct=[]
for item in items:
     linksToProduct.append(item.get_attribute("href"))

data = []
for link in linksToProduct:
    try:
        driver.get(link)
        
        time.sleep(1)
        
        productName = driver.find_element(By.CSS_SELECTOR, "h1.vtex-store-components-3-x-productNameContainer.vtex-store-components-3-x-productNameContainer--quickview").text
        
        brand=driver.find_element(By.CSS_SELECTOR,"span.vtex-store-components-3-x-productBrandName").text
       
        price = driver.find_element(By.CSS_SELECTOR,"span.vtex-product-price-1-x-currencyContainer").text
       
        subCategory1=driver.find_element(By.CSS_SELECTOR,"span.vtex-breadcrumb-1-x-arrow.vtex-breadcrumb-1-x-arrow--1").text
        subCategory2=driver.find_element(By.CSS_SELECTOR,"a.vtex-breadcrumb-1-x-link.vtex-breadcrumb-1-x-link--2").text
      
        data.append({"product_name": productName,"brand":brand,"price":price,"category":subCategory1 +" - "+ subCategory2})
       
    except:
        pass

driver.quit()


df = pd.DataFrame(data)
fileName="data.csv" #Acá puedes cambiar el nombre final del archivo generado.
df.to_csv(fileName, index=False, encoding='utf-8-sig')

print("✅ Datos guardados en"+" "+fileName)
