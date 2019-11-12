import urllib.request
from bs4 import BeautifulSoup

category_url = "https://www.newegg.com/zotac-geforce-gtx-1060-zt-p10620a-10m/p/N82E16814500454"

with urllib.request.urlopen(category_url) as read_file:
        soup = BeautifulSoup(read_file, "html.parser")

html = soup.prettify()
with open('soup.html', 'w') as outfile:
       outfile.write(html)