import requests
from bs4 import BeautifulSoup
import itertools


base_urls = []
for page in range(2, 3):
    base_urls.append(f'https://kazan.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&maxprice=3300000&minprice=1000000&offer_type=flat&p={str(page)}&region=4777&room1=1&room9=1')
def get_html(url):
    response = requests.get(url = url)
    soup = BeautifulSoup(response.text, 'html.parser')
    addres = soup.findAll('div', class_ = '_93444fe79c--labels--L8WyJ')
    urls = soup.findAll('a', class_ = '_93444fe79c--media--9P6wN')
    result_add = []
    result_urls = []
    result = []
    for item in addres:
        result_add.append(item.text)
    for url in urls:
        result_urls.append(url.get('href'))
    for i in range(len(result_urls)):
        result.append({'Адрес' : result_add[i], 'Ссылка' : result_urls[i]})
    return result

result_10_pages = [get_html(page) for page in base_urls]
result_10_pages = list(itertools.chain(*result_10_pages))
def addres_normal(result_10_pages):
    for i in result_10_pages:
        i['Адрес'] = i['Адрес'].split(',')[-2] + ', ' + i['Адрес'].split(',')[-1]
        i['Адрес'] = i['Адрес'].strip()
    return result_10_pages

normaled_addres = addres_normal(result_10_pages)
def get_coords(normaled_addres):
    bkrasnaya = {'lat': 55.796854, 'lon': 49.134337}
    for addres in normaled_addres:
        addres['Адрес'] = 'Казань, ' + addres['Адрес']
        response = requests.get(
            f'https://catalog.api.2gis.com/3.0/items/geocode?q={addres["Адрес"]}&fields=items.point&key=259008dc-94d3-402c-9789-daca4efba667').json()
        for i in response['result']['items']:
            addres['Координаты'] = i['point']
    return(normaled_addres)

coords = get_coords(normaled_addres)

print(coords)











