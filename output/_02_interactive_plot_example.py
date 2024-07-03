#!/usr/bin/env python
# coding: utf-8

# # Interactive Visualization Example
# 
# This example comes from here: https://jupyterbook.org/en/stable/interactive/interactive.html

# In[ ]:


import plotly.io as pio
import plotly.express as px
import plotly.offline as py

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", size="sepal_length")
fig


# In[ ]:




