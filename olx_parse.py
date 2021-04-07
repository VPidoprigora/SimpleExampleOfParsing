import requests
from bs4 import BeautifulSoup
import csv


def get_html(url): #get html-code of a page
    r = requests.get(url)
    return r.text

def get_total_pages(html): #accept the get_html() output

    soup = BeautifulSoup(html, 'lxml')

    pages = soup.find('div', class_="pager").find_all('a', class_='block')[-1].get('href')

    total_pages = pages.split('?page=')[1]

    return int(total_pages)


def write_csv(data, filename='olx.csv'):#wtite data to a csv file
    with open(filename, mode="w") as f:

        names = ["title", "price", "location", "time", "url"]
        writer = csv.DictWriter(f, delimiter=";",lineterminator="\r", fieldnames=names)

        writer.writeheader()

        for row in data:
            writer.writerow(row)


def get_page_data(html):#accept the html-code
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='listHandler').find_all('div', class_='offer-wrapper')

    data = []

    # get title, price, location, time, url
    for ad in ads:
        try:
            title = ad.find('a', class_='link').find('strong').text.strip()
        except:
            title = ''

        try:
            url = ad.find('a', class_='link').get('href')
        except:
            url = ''

        try:
            price = ad.find('p', class_='price').text.strip()
        except:
            price = ''

        try:
            location = ad.find('td', class_='bottom-cell').find_all('small', class_='breadcrumb')[0].text.strip()
        except:
            location = ''

        try:
            time = ad.find('td', class_='bottom-cell').find_all('small', class_='breadcrumb')[1].text.strip()
        except:
            time = ''

        local_data = {'title': title,
                      'price': price,
                      'location': location,
                      'time': time,
                      'url': url}

        data.append(local_data)

    return data


def main():

    url = 'https://www.olx.ua/elektronika/telefony-i-aksesuary/mobilnye-telefony-smartfony/apple/'

    total_pages = get_total_pages(get_html(url))

    base_url = 'https://www.olx.ua/elektronika/telefony-i-aksesuary/mobilnye-telefony-smartfony/apple/'
    page_part = '?page='

    data = []

    for i in range(1, total_pages):
        url_gen = base_url + page_part + str(i)
        data += get_page_data(get_html(url_gen))

    write_csv(data)


if __name__ == '__main__':
    main()
