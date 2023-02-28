import time
import requests
from googletrans import Translator
from bs4 import BeautifulSoup,Tag,NavigableString
import os
def scrape_file():
    url = 'https://www.classcentral.com'

    HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }

    html_tempalte = requests.get(url, headers=HEADERS).text

    with open('website/class_ce.html','w') as f:
        f.write(html_tempalte)
        

    soup = BeautifulSoup(html_tempalte, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        if not 'http' in link.get('href') or not 'cdn' in link.get('href') or link.get('href') != '/':
            urls.append(link.get('href'))
        

    url_lengh = len(urls)
    while url_lengh > 0:
        time.sleep(20)
        for url_link in urls:
            if not 'report' in url_link:
                url_tempalte = requests.get(f"{url}{url_link}", headers=HEADERS).text
                with open(f'website{url_link}.html','w') as f:
                    f.write(url_tempalte)
                    url_lengh -= 1
            
        

def trans_to_hindi(file):
    print(f'translating {file} to hindi')
    html = open(file).read()
    soup = BeautifulSoup(html,'html.parser')
    tags = soup.find_all(["p","ul","ol","h1","h2","h3","h4","h5","h6","td","title","button","span","strong","a"])
    translator=Translator()
    for tag in tags:
        for i in range(0, len(tag.contents)):
            if type(tag.contents[i])== NavigableString:
                try:
                    translation=translator.translate(tag.contents[i],dest="hi").text
                    tag.find(text=str(tag.contents[i])).replace_with(translation)
                except Exception as e:
                    print(f'failed to translate {e}')
        with open(file, "wb") as f_output:
            f_output.write(soup.prettify("utf-8"))
            
            
            
#scrape_file()

for root, dirs, files in os.walk('website'):
    for filename in files:
        trans_to_hindi(os.path.join(root, filename))
        
        
