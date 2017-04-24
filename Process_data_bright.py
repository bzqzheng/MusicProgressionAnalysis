
# coding: utf-8

# In[116]:

import pandas
pandas.set_option('display.max_rows',1000)
pandas.set_option('display.max_columns',10000)
import numpy


# In[117]:

m2016 = pandas.read_csv('music2016.csv')
m2016 = m2016.drop(m2016.columns[0], axis=1)


# In[172]:

# Pointwise Mutual Information calculator
# @Parameters:
#     - co_curr: number of counts of two words together
#     - a_curr: number of counts of word A (a_curr > co_curr)
#     - b_curr: number of counts of word B (b_curr > co_curr)
#     - doc_size: word population
def pmi(co_curr, a_curr, b_curr, doc_size):
    ratio = (co_curr*doc_size) / ((a_curr) * (b_curr))
    PMI = numpy.log(ratio)
    return PMI

# Converts chord list (input) into a set of chord pairs
# @Parameters:
#    - cd_list: chord list
def get_chord_pair_set(cd_list):
    result_pair = list()
    for i in range(0, len(cd_list)-1):
        temp_str = str(cd_list[i]+' '+cd_list[i+1])
        result_pair.append(temp_str)
    result_pair_set = set(result_pair)
    return result_pair_set

# Given a year, output a pandas data frame with 
def get_ranked_pair(year):
    file_name = 'music'+str(year)+'.csv'
    df = pandas.read_csv(file_name)
    df = df.drop(df.columns[0], axis=1)
    result_df = pandas.DataFrame()
    for i in range(0,len(df.chords)):
        col_name = i
        pair_set = get_chord_pair_set(str(df.chords[i]).split(' '))
        if len(pair_set) < 3:
            result_df[col_name] = ["", "", ""]
            continue
        pmi_pair = list()
        for pair in pair_set:
            co_curr = df.chords[i].count(pair)
            pair_list = pair.split(' ')
            a_curr = df.chords[i].split(' ').count(pair_list[0])
            b_curr = df.chords[i].split(' ').count(pair_list[1])
            doc_size = len(df.chords[i].split(' '))
            pmi_pair.append((pair, pmi(co_curr, a_curr, b_curr, doc_size)))            
        pmi_pair.sort(key=lambda p: p[1], reverse=True)
        pmi_pair = [str(pair[0]) for pair in pmi_pair]
        result_df[col_name] = pmi_pair[0:3]
        res_df = result_df.transpose()
        res_df.columns = ['top_1', 'top_2', 'top_3']
        comb_df = pandas.concat([df, res_df], axis=1)
    return comb_df


# In[173]:

def write_csv(i):
    file_name = 'music'+str(i)+'_chords.csv'
    get_ranked_pair(i).to_csv(file_name)


# In[175]:

for i in range(2006, 2016):
    write_csv(i)


# In[ ]:



