
# coding: utf-8

# In[32]:

import bs4
import requests
import pandas
pandas.set_option('display.max_rows',100)


# In[42]:

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
    chords_list = [word.replace('<span>', '').replace('</span>', '').replace('</pre>]', '') for word in str(content).split() if word[0:6] == '<span>']
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

# clean (artist, song title pair)
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


# In[28]:

top_list = get_top100(2015)


# In[29]:

result_list_2015 = list()
for song in top_list:
    query = clean_pair(song)
    search_result_url = search_url(query)
    search_result_soup = soup_page(search_result_url)
    if (not check_no_result(search_result_soup)):
        rows = get_rows(search_result_soup)
        max_rating = 0
        max_url = ""
        for row in rows:
            if get_type(row).lower() == 'chords' and get_rating(row) != None and get_rating(row) > max_rating:
                max_rating = get_rating(row)
                max_url = get_url(row)
        if (max_rating != 0):
            tt = (song[0], song[1], max_rating, max_url)
            result_list_2015.append(tt)

result_df = pandas.DataFrame(result_list_2015, columns=['artist', 'title', 'rating', 'url'])


# In[35]:

test_query = get_top100_query(2016)[0:2]
test_query


# In[43]:

for query in test_query:
    query_url = search_url(query)
    soup = soup_page(query_url)
    if (not check_no_result(soup)):
        rows = get_rows(soup)
        max_rating = 0
        max_url = ""
        for row in rows:
            if get_type(row).lower() == 'chords' and get_rating(row) != None and get_rating(row) > max_rating:
                max_rating = get_rating(row)
                max_url = get_url(row)
        print(max_url)
        chord_list = get_chords(max_url)
        print(chord_list)


# In[ ]:




# In[ ]:



