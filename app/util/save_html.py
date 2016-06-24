import requests

url = 'http://www.imdb.com/title/tt3659388/'
url = 'http://www.google.com/search?tbm=isch&q=kk'
headers = {'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64; '
                          'rv:34.0) Gecko/20100101 Firefox/34.0')}
r = requests.get(url, headers=headers)
with open('r.html', 'wb') as f:
	f.write(r.content)