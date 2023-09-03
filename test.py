import requests

url = 'https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=537021&xvyber=2108'
response = requests.get(url)
content_type = response.headers['Content-Type']
print(content_type)