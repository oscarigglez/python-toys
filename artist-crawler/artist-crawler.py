#!/anaconda3/bin/python

import csv
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Óscar Iglesias González',
    'From': 'oscarigglez@gmail.com'
    }

# create a csv file and add headers
f = csv.writer(open('z-artist-names.csv', 'w'))
f.writerow(['name', 'link'])

main = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ{}.htm'
pages = [main.format(i) for i in range(1,5)]

for url in pages:
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    # remove bottom links
    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    # pull all of the text from the div with class .BodyText
    artist_name_list = soup.find(class_='BodyText')

    # pull all of the a elements that are within .BodyText divs
    artist_name_list_items = artist_name_list.find_all('a')

    # print everything nicely
    for artist_name in artist_name_list_items:
        name = artist_name.contents[0]
        link = 'https://web.archive.org' + artist_name.get('href')
        f.writerow([name, link])
