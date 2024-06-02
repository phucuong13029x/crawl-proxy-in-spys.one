import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://spys.one/en/socks-proxy-list/"
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}
# data = {
#     'xx0': 'e30a37ef6e39aeeb1423b9cb2b6d2c4a',
#     'xpp': '5',
#     'xf1': '0',
#     'xf2': '0',
#     'xf4': '0',
#     'xf5': '2',
# }
# html_text = requests.post(url, headers=headers, data=data).text
html_text = requests.get(url, headers=headers).text
soup = BeautifulSoup(html_text, 'html.parser')
body = soup.find('body')
sc = body.find_all('script')[2]
sc = str(sc).replace('<script type="text/javascript">', '').replace(';</script>', '').split(';')[10:]
data = []
a = soup.find_all('table')[1]
b = a.find_all('table')[0]
c = b.find_all('tr')
for tr in c:
    row = []
    for td in tr.find_all('td'):
        r = td.text
        re_content = str(td)
        if re_content.find('<script type="text/javascript">document.write("<font class=spy2>:<\/font>"+') != -1:
            index_1 = re_content.find('<\/font>"+') + len('<\/font>"+')
            index_2 = re_content.find(')</script>')
            re_text = re_content[index_1:index_2]
            re_text = re_text.replace("(", "").replace(")", "").split("+")
            r_port = ':'
            for i in re_text:
                for k in sc:
                    if k.find(i[:i.find('^')]) != -1:
                        s = k.find('=') + 1
                        r_port += k[s: s + 1]
            if len(r_port) > 1:
                r += r_port
        row.append(r)
    if len(row) == 10:
        data.append(row)

df = pd.DataFrame(data, columns=['Proxy address:port', 'Proxy type', 'Anonymity', 'Country', 'Hostname', 'Latency', 'Speed', '*', 'Uptime', 'Check date'])
print(df)
