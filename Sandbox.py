
# coding: utf-8

# In[51]:

import bs4
import requests


# In[52]:

weekend = requests.get('https://www.ultimate-guitar.com/search.php?search_type=title&order=&value=I+feel+it+coming')
weekend_soup = bs4.BeautifulSoup(weekend.content, 'html.parser')


# In[63]:

def get_chords(web_url):
    req = requests.get(web_url)
    req_soup = bs4.BeautifulSoup(req.content, 'html.parser')
    content = req_soup.find_all('pre', {'class':'js-tab-content'})
    chords_list = [word.replace('<span>', '').replace('</span>', '') for word in str(content).split() if word[0:6] == '<span>']
    return chords_list


# In[64]:

url = ('https://tabs.ultimate-guitar.com/t/the_weeknd/i_feel_it_coming_ver2_crd.htm')
result = get_chords(url)
print(result)


# In[ ]:



