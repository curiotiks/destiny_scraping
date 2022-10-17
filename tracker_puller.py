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

rows = soup.find('tbody').find_all('tr')

for row in rows:
    
    cells = row.find_all('td')
    
    row_values['rank'] = cells[0].get_text().strip()
    row_values['platform'] = row.find('svg', class_='platform-icon')['class'][2].replace("platform-", "")
    row_values['player'] = cells[1].unicode_markup.get_text().strip()
    row_values['kd'] = cells[3].get_text().strip()
    row_values['rounds'] = cells[4].get_text().strip()
    
    player_row = pd.Series(row_values)
    data = data.append(player_row, ignore_index=True)
    
print(data.head())