
# coding: utf-8

# In[1]:

import pandas
pandas.set_option('display.max_rows',1000)
pandas.set_option('display.max_columns',10000)


# In[2]:

m2016 = pandas.read_csv('music2016.csv').drop
m2016


# In[11]:

m2016['chord_set'] = [set(chords.split(' ')) for chords in m2016.chords]


# In[22]:

m2016.chord_set[0].union(m2016.chord_set[1])


# In[23]:

m2016.chord_set[0]


# In[24]:

m2016.chord_set[1]


# In[26]:

vocab = m2016.chord_set[0]
for ss in m2016.chord_set:
    print(type(ss))
vocab


# In[ ]:



