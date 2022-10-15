from nis import cat
from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml

page = 1
url = 'https://destinytracker.com/destiny-2/leaderboards/stats/all/Kd?page=' + str(page)

pages = requests.get(url)
soup = BeautifulSoup(pages.text, 'lxml')

## USER NAMES
u_output = soup.find_all('span', class_='trn-ign__username')
user_list = []
users = pd.Series(dtype='str')

for i in u_output: 
    gamerTag = i.text.strip()
    user_list.append(gamerTag)
    
# users.str.encode(encoding = 'utf-8')

## PLATFORM
p_output = soup.find_all('svg', class_='platform-icon')
platform = []

for p in p_output:
    p.path.extract()
    icon = p['class'][2]
    icon = icon.replace("platform-", "")
    platform.append(icon)
    

data = {'GMRTAG': users,
        'PLTFRM': platform}

print(data)
# df = pd.DataFrame(data)


