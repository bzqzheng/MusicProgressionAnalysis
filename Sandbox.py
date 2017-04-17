
# coding: utf-8

# In[51]:

import bs4
import requests


# In[151]:

weekend = requests.get('https://www.ultimate-guitar.com/search.php?search_type=title&order=&value=I+feel+it+coming')
weekend_soup = bs4.BeautifulSoup(weekend.content, 'html.parser')


# In[344]:

def soup_page(web_url):
    req = requests.get(web_url)
    req_soup = bs4.BeautifulSoup(req.content, 'html.parser')
    return req_soup

# This function scrapes chords from a ultimate guitar website and
# returns a list of all the chords on that page
def get_chords(web_url):
    req_soup = soup_page(web_url)
    content = req_soup.find_all('pre', {'class':'js-tab-content'})
    chords_list = [word.replace('<span>', '').replace('</span>', '') for word in str(content).split() if word[0:6] == '<span>']
    return chords_list

def get_rating(row):
    temp_rate = row.find('td', {'class':'gray4 tresults--rating'})
    rate_list = temp_rate.find_all('b', {'class':'ratdig'})
    if (len(rate_list) > 0):
        rate = rate_list[0].text.strip()
        return float(rate)

def get_type(row):
    row_type = row.find_all('strong')[0].text.strip()
    return row_type

# -- Puyush's functions --
def get_url(row):
    search_version = row.find_all('td',{'class':'search-version--td'})[0]
    href = search_version.find_all('a')[0].attrs['href']
    return href

def get_bbd_year_url(year_input):
    url = 'http://www.billboard.com/charts/year-end/'
    url += str(year_input)
    url += '/hot-100-songs'
    return url

def update_url(int_year):
    billboard = requests.get(get_bbd_year_url(int_year))
    billboard_soup = bs4.BeautifulSoup(billboard.content, 'html.parser')
    innerContent =  billboard_soup.find_all('div', {'data-content-type': 'yearEndChart'})
    artistData = innerContent[0].find_all('div' , {'class': 'ye-chart__layout-row'})
    artistData = artistData[1:]
    return artistData

def data(row):
    p = list()
    article = row.find_all('article', {'id': 'chart'})
    for i in range(len(article)):
        article_chart = article[i].find_all('div', {'class': 'ye-chart__item-primary'})
        songTitle = article_chart[0].find_all('h1', {'class':'ye-chart__item-title'})[0].text.strip()
        artistName = article_chart[0].find_all('h2', {'class':'ye-chart__item-subtitle'})[0].text.strip()
        p.append((artistName, songTitle))
    return p

def get_top100(int_year):
    pairs = list()
    top100Songs = list()
    pairs = [data(d) for d in update_url(int_year)]
    for p in pairs:
        top100Songs += p
    return top100Songs


# In[331]:

hello = 'https://www.ultimate-guitar.com/search.php?search_type=title&order=&value=hello+adele'
feel_coming = 'https://www.ultimate-guitar.com/search.php?search_type=title&order=&value=i+feel+it+coming'
sorry = 'https://www.ultimate-guitar.com/search.php?search_type=title&order=&value=sorry+justin+bieber'
search_soup = soup_page(sorry)
table = search_soup.find_all('table',{'class':'tresults'})[0]


# In[332]:

rows = table.find_all('tr')[1:len(table)]


# In[334]:

for row in rows:
    if get_type(row) == 'chords':
        if (get_rating(row) != None):
            print(get_rating(row),"\t", get_url(row))


# In[345]:

get_top100(2010)


# In[ ]:



