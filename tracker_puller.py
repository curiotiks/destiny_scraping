from nis import cat
from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml

url = 'https://destinytracker.com/destiny-2/leaderboards/stats/all/Kd?page='
data = pd.DataFrame()

def make_soup(url=url, page_number=1):
    page = requests.get(url + str(page_number))
    soup = BeautifulSoup(page.text, 'lxml')
    return soup

## Make soup and select the first row of table
soup = make_soup()
table = soup.tbody.tr

row_values = {
    'rank':     None, 
    'platform': None,
    'player':   None, 
    'kd':       None, 
    'rounds':   None
}

row_values['rank'] = table.find('td', class_='rank').text.strip()
row_values['platform'] = table.find('svg', class_='platform-icon')['class'][2].replace("platform-", "")
row_values['player'] = table.find('td', class_='username').text.strip()
row_values['kd'] = table.find('td', class_='stat highlight').text.strip()
row_values['rounds'] = table.find('td', class_='stat collapse').text.strip()

## Build list above and then add to series below
player_row = pd.Series(row_values)
data = data.append(player_row, ignore_index=True)
data = data.set_index('rank')

print(data.head())

## Now I have one row. Stop bothering with the encoding issue and work on iterating across pages!