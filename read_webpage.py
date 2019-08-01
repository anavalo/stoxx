import csv
import warnings
import requests
from bs4 import BeautifulSoup
import time
from json import loads
import re
from datetime import datetime
from requests import RequestException

CAPITAL_URL = 'https://www.capital.gr/'

class Document:
    #ftiakse an thes mia class edw gia na mproyme na to genikeuoyme se alla sites
    def __init__(self, text, date, tags):
        pass


def read_news_from_capital():
    dates_dict = {'Ιαν': '01',
                  'Φεβ': '02',
                  'Μαρ': '03',
                  'Απρ': '04',
                  'Μαϊ': '05',
                  'Ιουν': '06',
                  'Ιουλ': '07',
                  'Αυγ': '08',
                  'Σεπ': '09',
                  'Οκτ': '10',
                  'Νοε': '11',
                  'Δεκ': '12'}

    with open('news2.csv', 'w', encoding="utf-8", newline='') as f:
        csvwriter = csv.writer(f, delimiter='\t')
        csvwriter.writerow(['date','tags','news'])
        for i in range(3023161, 3353915):
            try:
                query = requests.get(CAPITAL_URL + str(i))
                if query.status_code == 200 and CAPITAL_URL in query.text:
                    soup = BeautifulSoup(query.text, 'html.parser')

                    data = []
                    for div in soup.find_all('div'):
                        values = [p.text for p in div.find_all('p')]
                        data.append(values)
                    news = [x for x in data if x != []]
                    news = news[0][0:]
                    news = ''.join(news).replace('\n', ' ')
                    sliced_date = ''
                    for div in soup.find_all('div', attrs={'class': 'article__content'}):
                        for h5 in div.find_all('h5')[0]:
                            sliced_date = str(h5)[-18:]
                            sliced_date = sliced_date[:12]
                    for k, v in dates_dict.items():
                        sliced_date = sliced_date.replace(k, v).replace(' ', '')
                    oldformat = sliced_date
                    try:
                        datetimeobject = datetime.strptime(oldformat, '%d-%m-%Y')
                        newformat = datetimeobject.strftime('%d/%m/%Y')
                        date = newformat
                    except:
                        date = oldformat

                    script_text = soup.find("script", text=re.compile("var\s+dataLayer")).text.split("= ", 1)[1]
                    json_data = loads(script_text[:script_text.find(";")])
                    tags_per_doc = ''
                    if 'keywords' in json_data[0]['page']:
                        keywords = (json_data[0]['page']['keywords'])
                        if type(keywords) == list:
                            tags_per_doc = ','.join(keywords)
                        else:
                            tags_per_doc = keywords
                    csvwriter.writerow([date, news, tags_per_doc])
                else:
                    continue
            except RequestException:
                warnings.warn('Failed to get URL: ' + str(i))
            time.sleep(0.15)
if __name__ == '__main__':
    read_news_from_capital()
