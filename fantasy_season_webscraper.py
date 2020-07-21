from sys import argv
from requests import get
import pandas as pd
from bs4 import BeautifulSoup

"""
Create virtual environment
>python -m venv venv
>source venv/bin/activate (linux/mac)
>venv\Scripts\activate

pip install requests
pip install beautifulsoup4
pip install html5lib
pip install pandas

"""
#find out the year that we want to look at
year = input("Which season's stats would you like? (1999 onwards) ")

year = int(year)

#identify the url
url = 'https://www.pro-football-reference.com/years/{}/fantasy.htm'.format(year)

#default column settings to make dropping and changing columns easier
defColumnSettings = {'axis':1, 'inplace':True}

#find the table
response = get(url)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table', {'id': 'fantasy'})

#creating the data frame
df = pd.read_html(str(table))[0]
df.columns = df.columns.droplevel(level=0)
df = df[df['Tm'] != 'Tm']
df.fillna(0, inplace=True)
df['Player'] = df['Player'].map(lambda x: x.rstrip('*+'))

try:
    if argv[1] == '--save':
        df.to_csv('datasets/full season stats/fantasy/{y}_fantasy_stats.csv'.format(y = year))
except IndexError:
    pass
