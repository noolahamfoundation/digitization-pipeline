#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd


# In[3]:


df = pd.read_csv('repo_data_1.csv', sep=',')
df1 = pd.read_csv('repo_data_2.csv', sep=',')
df2 = pd.read_csv('repo_data_3.csv', sep=',')
df3 = pd.read_csv('repo_data_4.csv', sep=',')


# In[4]:


df_combined = pd.concat([df,df1,df2,df3])


# In[5]:


df_combined.to_csv('aavanaham_jan_12.csv')


# In[ ]:




