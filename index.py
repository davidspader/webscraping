import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
 
navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
 
tabela = pd.read_excel('commodities.xlsx')

for linha in tabela.index:
    produto = tabela.loc[linha, "Produto"]
    produto = produto.replace("ó", "o").replace("ã", "a").replace("á", "a").replace(
    "ç", "c").replace("ú", "u").replace("é", "e")

    link = f"https://www.melhorcambio.com/{produto}-hoje"
    navegador.get(link)

    preco = navegador.find_element('xpath', '//*[@id="comercial"]').get_attribute('value')
    preco = preco.replace(".", "").replace(",", ".")
    tabela.loc[linha, "Preço Atual"] = float(preco)

tabela["Comprar"] = tabela["Preço Atual"] < tabela["Preço Ideal"]

tabela.to_excel("commodities_atualizado.xlsx", index=False)