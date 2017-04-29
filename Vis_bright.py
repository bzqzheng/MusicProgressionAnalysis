
# coding: utf-8

# In[276]:

import pandas
pandas.set_option('display.max_rows',1000)
pandas.set_option('display.max_columns',10000)
import math


# In[277]:

def clean_dict_func(input_dict):
    return dict((k, v) for k, v in input_dict.items() if not (type(k) == float and math.isnan(k)))

def get_year_dict(int_year):
    file_name = 'music'+str(int_year)+'_chords.csv'
    df = pandas.read_csv(file_name)
    df = df.drop(df.columns[0], axis=1)
    index = 0
    temp_dict = dict()
    for index in range(0, len(df)):
        row = df.iloc[index]
        top1 = row['top_1']
        top2 = row['top_2']
        top3 = row['top_3']
        if top1 in temp_dict:
            temp_dict[top1] = temp_dict[top1] + (1000 - index*10)
        else:
            temp_dict[top1] = 1000 - index*10
        if top2 in temp_dict:
            temp_dict[top2] = temp_dict[top2] + (1000 - index*10) - 2
        else:
            temp_dict[top2] = 1000 - index*10 - 2
        if top3 in temp_dict:
            temp_dict[top3] = temp_dict[top3] + (1000 - index*10) - 3
        else:
            temp_dict[top3] = 1000 - index*10 - 3
    clean_dict = clean_dict_func(temp_dict)
    temp_df = pandas.DataFrame()
    temp_df = temp_df.from_dict(clean_dict, orient='index')
    temp_col_name = 'year_'+str(int_year)
    temp_df.columns = [temp_col_name]
    temp_df = temp_df.sort_values(temp_col_name, ascending=False)
    return temp_df


# In[278]:

final_df = get_year_dict(2016)


# In[279]:

for i in range(2006, 2016):
    final_df = final_df.join(get_year_dict(i))


# In[282]:

final_df = final_df.fillna(0)


# In[283]:

import 


# In[ ]:



