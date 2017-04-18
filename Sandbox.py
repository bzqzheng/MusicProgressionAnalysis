
# coding: utf-8

# In[456]:

import bs4
import requests
import pandas


# In[452]:

# Returns the Beautifulsoup of the input 'web_url'
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

# Check whether a certain query has any result on ultimate guitar
# return false if there is at least one result, true otherwise
def check_no_result(soup_result):
    not_found = soup_result.find_all('div',{'class':'not_found'})
    return len(not_found) != 0

# Returns the table of different versions from the search page
def get_table(soup_result):
    return soup_result.find_all('table', {'class':'tresults'})[0]

# Returns a list of rows
def get_rows(soup_result):
    return get_table(soup_result).find_all('tr')[1:len(get_table(soup_result))]

# Returns the rating of a certain row in the ultimate guitar result page
def get_rating(row):
    temp_rate = row.find('td', {'class':'gray4 tresults--rating'})
    rate_list = temp_rate.find_all('b', {'class':'ratdig'})
    if (len(rate_list) > 0):
        rate = rate_list[0].text.strip()
        return float(rate)

# Returns the type of a certain row in a result page
def get_type(row):
    row_type_list = row.find_all('strong')
    if (len(row_type_list) > 0):
        row_type = row_type_list[0].text.strip()
        return row_type

# Return the url of a certain row (version) of chords in a result page
def get_url(row):
    search_version = row.find_all('td',{'class':'search-version--td'})[0]
    href = search_version.find_all('a')[0].attrs['href']
    return href

# Gets the top 100 songs from Billboard of the input year
def get_top100(int_year):
    pairs = list()
    top100Songs = list()
    pairs = [data(d) for d in update_bbd_url(int_year)]
    for p in pairs:
        top100Songs += p
    return top100Songs

# Converts the top 100 songs in a particular year into
# a searchable string
def get_top100_query(int_year):
    if (int_year > 2016): int_year = 2016
    elif (int_year < 2006): int_year = 2006
    top100 = get_top100(int_year)
    result = [clean_pair(pair) for pair in top100]
    return result

def clean_pair(pair):
    return clean_name(pair[0]) + ' ' + clean_name(pair[1])

# Clean up both artist name and song titles from get_top100() list
def clean_name(str_input):
    return str_input.lower().replace('(','').replace(')','').replace('&','').split('featuring',1)[0]

# Generates a search result page based on the input
# The url can be both a list of different versions of chords
# or "No Result" page
def search_url(str_query):
    root = 'https://www.ultimate-guitar.com/search.php?search_type=title&order=&value='
    str_query = str_query.replace(' ', '+')
    return root+str_query

# -- Puyush's functions --
def get_bbd_year_url(year_input):
    url = 'http://www.billboard.com/charts/year-end/'
    url += str(year_input)
    url += '/hot-100-songs'
    return url

def update_bbd_url(int_year):
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
# -- End of Puyush's functions --


# In[450]:

query_list = get_top100_query(2016)
for pair in query_list:
    pair_soup = soup_page(search_url(pair))
    if (not check_no_result(pair_soup)):
        rows = get_rows(pair_soup)
        print(pair)
        for row in rows:
            row_type = get_type(row)
            row_rating = get_rating(row)
            if row_type == 'chords' and row_rating != None:
                print('\t' + str(get_rating(row)) + ' ' + get_url(row))


# In[461]:

top_list = get_top100(2016)
total = pandas.DataFrame(columns=('artist','title','rating','link'))


# In[463]:

total_list = list()
for pair in query_list:
    pair_soup = soup_page(search_url(pair))
    if (not check_no_result(pair_soup)):
        pair_list = list()
        rows = get_rows(pair_soup)
        pair_list.append(pair)
        for row in rows:
            row_type = get_type(row)
            row_rating = get_rating(row)
            if row_type == 'chords' and row_rating != None:
#                 print('\t' + str(get_rating(row)) + ' ' + get_url(row))
                pair_list.append(str(get_rating(row)))
                pair_list.append(str(get_url(row)))
        total_list.append(pair_list)


# In[465]:

kk = pandas.DataFrame(total_list)


# In[466]:

kk


# In[483]:

top_list = get_top100(2016)[0:5]
total = pandas.DataFrame(columns=('artist','title','rating','link'))
total_list = list();
for pair in top_list:
    query_pair = clean_pair(pair)
    pair_soup = soup_page(search_url(query_pair))
    if (not check_no_result(pair_soup)):
        rows = get_rows(pair_soup)
        temp_list = list()
        for row in rows:
            row_type = get_type(row)
            row_rating = get_rating(row)
            if row_type == 'chords' and row_rating != None:
                temp_list.append(pair[0])
                temp_list.append(pair[1])
                temp_list.append(row_rating)
                temp_list.append(str(get_url(row)))
                temp_list.sort_values(temp_list[2])
    total_list.append(temp_list)


# In[484]:

total_list


# In[485]:

cc = pandas.DataFrame(total_list)
cc


# In[ ]:




# In[ ]:



