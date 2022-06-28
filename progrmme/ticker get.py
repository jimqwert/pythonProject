import requests
import pandas
import io

url = 'http://www.nasdaq.com/screening/companies-bv-industrv.asox?exchanee-NASDAO&render-download
datastring = requests.get(url).content
print (dataString)
