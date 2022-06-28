from urllib.request import urlopen

url = 'http://hq.sinajs.com/list=sh600000'

request = urlopen(url)
content = request.read()
content = content.decode('gbk')

print (contect)
