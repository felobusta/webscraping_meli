# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 13:59:01 2024

@author: fnbus
"""
#cargar paquetes
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime

# definir webdriver. usaremos chrome
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://listado.mercadolibre.cl/celulares")

#hay dos banners ahora que pueden molestar, uno de aceptar cookies y otro de aceptar definir direccion de entrega
# banner de cookies
cookie_banner_xpath = "//button[@data-testid='action:understood-button']"
cookie_banner_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, cookie_banner_xpath)))
cookie_banner_button.click()

# banner de direccion de entrega
mas_tarde_button_xpath = "//button[@class='onboarding-cp-button andes-button andes-button--transparent andes-button--small' and @data-js='onboarding-cp-close']"
mas_tarde_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, mas_tarde_button_xpath)))
mas_tarde_button.click()

# crear listas para alojar los datos
product_names = []
product_prices = []
product_links = []
extraction_datetime = []

# iterar 5 veces, siempre una más que la cantidad de páginas a extraer ya que la última página que vemos no es usada para descargar datos
for _ in range(5):  # 
    # obtener datos de página
    product_elements = driver.find_elements(By.XPATH, "//li[contains(@class, 'ui-search-layout__item')]")
    product_names_elements = driver.find_elements(By.XPATH, "//h2[@class='ui-search-item__title']")
    product_prices_elements = driver.find_elements(By.CSS_SELECTOR, ".ui-search-price__part--medium .andes-money-amount__fraction")

    # guardar datos en listas
    for product, name_element, price_element in zip(product_elements, product_names_elements, product_prices_elements):
        link_element = product.find_element_by_xpath(".//a[contains(@class, 'ui-search-link')]")
        product_links.append(link_element.get_attribute("href"))

        product_names.append(name_element.text)
        product_prices.append("$" + price_element.text)
        extraction_datetime.append(datetime.now())  

    # apretar boton siguiente
    
    siguiente_button_xpath = "//li[@class='andes-pagination__button andes-pagination__button--next']/a[@class='andes-pagination__link' and @title='Siguiente']"
    siguiente_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, siguiente_button_xpath)))
    siguiente_button.click()

# cerrar navegador
driver.quit()

# crear dataframe
df_final = pd.DataFrame({
    "Product Name": product_names,
    "Price": product_prices,
    "Extraction Datetime": extraction_datetime,
        "Product Link": product_links

})

# ver y guardar
print(df_final)

df_final.to_excel('datos_celulares.xlsx',index=True)

#obtener pool de marcas
#link de pool de marcas
driver.get("https://listado.mercadolibre.cl/celulares_FiltersAvailableSidebar?filter=BRAND")

# obtener elementos de nombre de marca con xpath
elements = driver.find_elements_by_xpath("//a[@class='ui-search-search-modal-filter ui-search-link']/span[@class='ui-search-search-modal-filter-name']")

# extraer el testo
text_list = [element.text for element in elements]

# crear dataframe
df = pd.DataFrame({"Marca": text_list})

#ver dataframe
print(df)
#guardar dataframe
df.to_excel('marcas_celulares.xlsx',index=True)

# cerrar navegador
driver.quit()
