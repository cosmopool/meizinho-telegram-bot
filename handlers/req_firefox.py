import asyncio
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CNPJ = "30.957.53/0001-05"
CNPJ = "12.291.315/0001-14"
URL_EMISSAO = "http://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/emissao"
URL_RECEITA = "http://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/Identificacao/"
dt = datetime(2022, 3, 10)

options = webdriver.FirefoxOptions()
# options.headless = True
options.set_preference("browser.download.folderList",2)
options.set_preference("browser.download.manager.showWhenStarting",False)
options.set_preference("browser.download.dir", "/home/kaio/tmp")
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
options.set_preference('useAutomationExtension', False)
options.set_preference("dom.webdriver.enabled", False);
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 5.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36")
# options.set_preference("network.proxy.type", 1);
# options.set_preference("network.proxy.http", "127.0.0.1");
# options.set_preference("network.proxy.http_port", "9050");
driver = webdriver.Firefox(options=options)

async def wait_for_element_to_load(driver, element: tuple, seconds = 5) -> None:
    """Wait for an especific html element load"""

    WebDriverWait(driver, seconds).until(EC.presence_of_element_located(element))


async def wait_for_element_and_click(driver, element: tuple, seconds = 5) -> None:
    """Wait for an especific html element load and then click on it"""

    WebDriverWait(driver, seconds).until(EC.element_to_be_clickable(element)).click()


async def get_document(driver, cnpj, url_receita) -> None:
    """Get a guia MEI pdf document and save to disk"""

    driver.get(url_receita)
    assert 'PGMEI - Programa Gerador de DAS do Microempreendedor Individual' in driver.title

    cnpj_input = driver.find_element(by='id', value='cnpj')
    cnpj_input.send_keys(cnpj)
    
    await wait_for_element_and_click(driver, (By.ID, 'continuar'))
    
    await wait_for_element_and_click(driver, (By.CLASS_NAME, 'glyphicon.glyphicon-check'))
    
    await wait_for_element_and_click(driver, (By.CLASS_NAME, 'form-control'))
    
    await wait_for_element_and_click(driver, (By.LINK_TEXT, "2022"))
    
    await wait_for_element_and_click(driver, (By.CLASS_NAME, "btn-success"))
    
    await wait_for_element_and_click(driver, (By.CLASS_NAME, "form-inline"))
    list_of_months = driver.find_elements(By.TAG_NAME, "tbody")
    
    for month in list_of_months:
        try:
            date = month.find_element(By.CLASS_NAME, "vencimento")
            due_date = datetime.strptime(date.text, '%d/%m/%Y')
        except:
            pass
        else:
            if due_date > dt:
                print(f"guia vencida: {date.text}. Preparando download...")
                month.find_element(By.TAG_NAME, "input").click()
    
            await wait_for_element_and_click(driver, (By.ID, "btnEmitirDas"))
    
    await wait_for_element_and_click(driver, (By.CLASS_NAME, "btn.btn-success"))

asyncio.run(get_document(driver, CNPJ, URL_RECEITA))
