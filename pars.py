import requests
from bs4 import BeautifulSoup as bs
import datetime
from datetime import timedelta
import constaints


def pars_site(site_url):
    session = requests.session()
    request = session.get(site_url)
    pars_data = []
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all(class_='el-row')
        for div in divs:
            wrapper = []
            event_url = div.find('a')['href']
            name = div.find(class_='el-info').find('a', text=True).text.replace('\n', ' ').strip()
            theme = 'Категория: ' + div.find(class_='el-info').find('span', text=True).text.replace('\n', ' ').strip()
            start_time = div.find(class_='el-info').find('p').text.replace('\n', '').strip()[6:]
            where = div.find('a', class_='el-club').text.replace('\n', ' ').strip()
            image = div.find('a').find('img')['data-normal']
            if div.find(class_='el-price').find('b') is None:
                price = 'Продано'
            else:
                price = 'от ' + div.find(class_='el-price').find('b').text.replace('\n', ' ').replace('-', 'до')\
                    .strip() + ' грн.'
            wrapper.append(event_url)
            wrapper.append(name)
            wrapper.append(theme)
            wrapper.append(price)
            wrapper.append(start_time)
            wrapper.append(where)
            wrapper.append(image)
            pars_data.append(wrapper)
    else:
        return None
    return pars_data


def today():
    today_date = datetime.date.today().strftime('%d.%m.%Y')
    url = constaints.site_url + f'{today_date}-{today_date}/'
    return pars_site(url)


def tomorrow():
    tomorrow_date = (datetime.date.today() + timedelta(days=1)).strftime('%d.%m.%Y')
    url = constaints.site_url + f'{tomorrow_date}-{tomorrow_date}/'
    return pars_site(url)
