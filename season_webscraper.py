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
year = input('Which season would you like to look into? (1999-2019) ')

year = int(year)

#identify the urls
passingURL = 'https://www.pro-football-reference.com/years/{}/passing.htm'.format(year)
receivingURL = 'https://www.pro-football-reference.com/years/{}/receiving.htm'.format(year)
rushingURL = 'https://www.pro-football-reference.com/years/{}/rushing.htm'.format(year)

urls = {
'passing': passingURL,
'rushing': rushingURL,
'receiving': receivingURL
}

dfs = []

#default column settings to make dropping and changing columns easier
defColumnSettings = {'axis':1, 'inplace':True}

#iterate through the key, value pairs in the urls dictionary to scrape the tables from pro football reference
for key, url in urls.items():
    response = get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': key})
    #creating the data frame
    df = pd.read_html(str(table))[0]

    if key == 'rushing':
        df.columns = df.columns.droplevel(level=0)

    df = df[df['Tm'] != 'Tm']

    df.set_index(['Player', 'Age', 'Pos', 'Tm', 'G'], inplace=True)
    #look into data tables to see how each key's table needs to be adjusted
    if key == 'passing':
        df = df[['Yds', 'TD', 'Int', 'Att', 'Cmp']]
        df.rename({'Yds': 'PassingYds', 'Att': 'PassingAtt', 'TD': 'PassingTD'}, **defColumnSettings)
    elif key =='receiving':
        df = df[['Rec', 'Tgt', 'Yds', 'TD']]
        df.rename({'Yds': 'ReceivingYds', 'TD': 'ReceivingTD'}, **defColumnSettings)
    elif key == 'rushing':
        df = df[['Yds', 'Att', 'TD']]
        df.rename({'Att': 'RushingAtt', 'Yds': 'RushingYds', 'TD': 'RushingTD'}, **defColumnSettings)
    dfs.append(df)


df = dfs[0].join(dfs[1:], how='outer')
df.fillna(0, inplace=True)
df = df.astype('int64')

#df['FantasyPoints'] = df['PassingYds']/25 + df['PassingTD']*4 - df['Int']*2 + df['Rec'] + df['ReceivingYds']/10 + df['ReceivingTD']*6 + df['RushingYds']/10 + df['RushingTD']*6

df.reset_index(inplace=True)

try:
    if argv[1] == '--save':
        df.to_csv('datasets/full season stats/NFL/{y}_season_player_stats.csv'.format(y = year))
except IndexError:
    pass
