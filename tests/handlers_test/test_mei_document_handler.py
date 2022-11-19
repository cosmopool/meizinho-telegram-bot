import requests
from handlers.mei_document_handler import URL_RECEITA

def test_fazenda_url():
    res = requests.get(URL_RECEITA)
    print(res)
