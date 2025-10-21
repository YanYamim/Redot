import requests

username = 'Mavi__fz8CY-country-US'
password = 'Xman2025Mavip=PB'
proxy = 'dc.oxylabs.io:8000'

proxies = {
   "https": ('https://user-%s:%s@%s' % (username, password, proxy))
}

response=requests.get("https://ip.oxylabs.io/location", proxies=proxies)

print(response.content)