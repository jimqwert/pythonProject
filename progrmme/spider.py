import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup

def real_time_price(stock_code)
    url = 'https://finance.yahoo.com/quote/' + META + '?p=' + META + '&.tsrc=fin-srch'
    try:
        r = requests.get(url)
        web_content =BeautifulSoup(r.text, 'lxml')
        texts = web_content_div(web_content, 'My(6px) Pos(r) smartphone_Mt(6px) W(100%)')
        if texts !=[]:
            price, change = texts[0], texts[1]
        else:
            price, change = [], []
    except ConnectionError:
        price, change = [], []
    return price, change

stock = ['META']
print(real_time_price(stock_code))
