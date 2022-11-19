import asyncio
import time
import os
import logging as log
from datetime import datetime
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CNPJ = "00.000.000/0001-00"
URL_EMISSAO = "http://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/emissao"
URL_RECEITA = "http://www8.receita.fazenda.gov.br/SimplesNacional/Aplicacoes/ATSPO/pgmei.app/Identificacao/"
DOWNLOAD_PATH = "/home/arrow/tmp"
log.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=log.INFO)
log.getLogger("seleniumwire.handler").disabled = True
log.getLogger("seleniumwire.storage").disabled = True
log.getLogger("seleniumwire.backend").disabled = True

def get_webdriver():
    """WebDriver configuration"""
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-notifications")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_PATH,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
        "plugins.always_open_pdf_externally": True,
    })
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    enable_download_headless(driver, DOWNLOAD_PATH)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 5.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})

    return driver

def enable_download_headless(browser, download_dir):
    """WebDriver headless configuration to be able to download files"""
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)


async def wait_download_complete(response_header: dict) -> str:
    """Wait for download file to complete by checking if file is on disk."""
    log.info("Checking document name")

    content_disposition = response_header.get('Content-Disposition')
    file_name = str(content_disposition).replace("attachment; filename=", "")
    path_to_file = DOWNLOAD_PATH + f"/{file_name}"

    log.debug(f"path to file: {path_to_file}")
    log.info("...Downloading file...")
    while not os.path.exists(path_to_file):
        time.sleep(.1)

    if os.path.isfile(path_to_file):
        log.info("File download is completed")
        return path_to_file
    else:
        log.error("Could not download file")
        return ""

async def wait_for_element_to_load(driver, element: tuple, seconds = 5) -> None:
    """Wait for an especific html element load"""

    WebDriverWait(driver, seconds).until(EC.presence_of_element_located(element))


async def wait_for_element_and_click(driver, element: tuple, seconds = 5) -> None:
    """Wait for an especific html element load and then click on it"""

    WebDriverWait(driver, seconds).until(EC.element_to_be_clickable(element)).click()


async def get_document(driver, cnpj: str, date: str) -> str:
    """Get a 'guia MEI' pdf document and save to disk"""
    found_document_to_download = False
    path_to_file = ""
    dt = datetime.now()

    driver.get(URL_RECEITA)
    log.info(f"Loading web site...")
    assert 'PGMEI - Programa Gerador de DAS do Microempreendedor Individual' in driver.title

    cnpj_input = driver.find_element(by='id', value='cnpj')
    cnpj_input.send_keys(cnpj)
    await wait_for_element_and_click(driver, (By.ID, 'continuar'))
    log.info(f"Sign in with: {cnpj}")
    
    await wait_for_element_and_click(driver, (By.CLASS_NAME, 'glyphicon.glyphicon-check'))
    
    await wait_for_element_and_click(driver, (By.CLASS_NAME, 'form-control'))
    
    log.info(f"Selecting given year")
    await wait_for_element_and_click(driver, (By.LINK_TEXT, date))
    
    await wait_for_element_and_click(driver, (By.CLASS_NAME, "btn-success"))
    
    await wait_for_element_and_click(driver, (By.CLASS_NAME, "form-inline"))
    list_of_months = driver.find_elements(By.TAG_NAME, "tbody")
    
    log.info(f"Searching document to download")
    for month in list_of_months:
        try:
            date_element = month.find_element(By.CLASS_NAME, "vencimento")
            due_date = datetime.strptime(date_element.text, '%d/%m/%Y')
        except:
            pass
        else:
            if due_date > dt or due_date < dt:
                log.info(f"Found document to download: {date_element.text}")
                found_document_to_download = True
                month.find_element(By.TAG_NAME, "input").click()
    
            await wait_for_element_and_click(driver, (By.ID, "btnEmitirDas"))
    
    if found_document_to_download:
        await wait_for_element_and_click(driver, (By.CLASS_NAME, "btn.btn-success"))
        path_to_file = await wait_download_complete(driver.requests[-1].response.headers)
    else:
        log.error("Did not found any document to download!")

    driver.close()
    
    if path_to_file == "":
        raise Exception("Could not download file")
    else:
        return path_to_file

# driver = get_webdriver()
# asyncio.run(get_document(driver, CNPJ, "2022"))
