
# coding: utf-8

# In[51]:

import bs4
import requests


# In[151]:

weekend = requests.get('https://www.ultimate-guitar.com/search.php?search_type=title&order=&value=I+feel+it+coming')
weekend_soup = bs4.BeautifulSoup(weekend.content, 'html.parser')


# In[260]:

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
    rate = temp_rate.find_all('b', {'class':'ratdig'})[0].text.strip()
    return float(rate)

def get_type(row):
    row_type = row.find_all('strong')[0].text.strip()
    return row_type


# In[235]:

search_link = 'https://www.ultimate-guitar.com/search.php?search_type=title&order=&value=i+feel+it+coming'
search_soup = soup_page(search_link)
table = search_soup.find_all('table',{'class':'tresults'})[0]


# In[251]:

rows = table.find_all('tr')[1:len(table)]
row0 = rows[4]


# In[262]:

for row in rows:
    if get_type(row) == 'chords':
        print(get_rating(row))


# In[ ]:



