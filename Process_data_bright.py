
# coding: utf-8

# In[84]:

import pandas
pandas.set_option('display.max_rows',1000)
pandas.set_option('display.max_columns',10000)
import collections


# In[57]:

m2016 = pandas.read_csv('music2016.csv')
m2016 = m2016.drop(m2016.columns[0], axis=1)
m2016


# In[58]:

m2016['chord_set'] = [set(chords.split(' ')) for chords in m2016.chords]
cd_2016_set = set().union(*m2016.chord_set)


# In[59]:

cd_2016_set


# In[80]:

chord_pair = list()
for chords in m2016.chords:
    cd_list = chords.split(' ')
    for index in range(0,len(cd_list)-1):
        temp_str = str(cd_list[index] + ' ' + cd_list[index+1])
        chord_pair.append(temp_str)
set(chord_pair)


# In[110]:

cd0 = m2016.chords[0]
cd_pair = list()
cd0_list = cd0.split(' ')
for i in range(0, len(cd0_list)-1):
    temp_str = str(cd0_list[i] + ' ' + cd0_list[i+1])
    cd_pair.append(temp_str)
cd_pair_set = set(cd_pair)


# In[112]:

cd_pair_set


# In[113]:

cd_pair


# In[ ]:



