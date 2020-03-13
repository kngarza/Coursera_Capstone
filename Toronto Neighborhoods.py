#!/usr/bin/env python
# coding: utf-8

# # Segmenting and Clustering Neighborhoods in Toronto

# ## Introduction

# ### In this assignment, I will explore, segment, and cluster the neighborhoods in the city of Toronto. However, the neighborhood data is not readily available onthe internet. For the Toronto neighborhood data, a Wikipedia page exists that has all the information I need to explore and cluster the neighborhoodsin Toronto. I will scrape the Wikipedia page and wrangle the data, clean it,and then read it into a pandas dataframe so that it is in a structured format. 

# ### First, I will use this Notebook to build the code to scrape the Wikipedia page in order to obtain the data that is in the table of postal codes and to transform the data into a pandas dataframe. 

#   * The dataframe will consist of three columns: PostalCode, Borough, and Neighborhood
#   * I only process the cells that have an assigned borough. I ignore cells with a borough that is Not assigned.
#   * More than one neighborhood can exist in one postal code area. For example, in the table on the Wikipedia page, you will notice that M5A is listed twice and has two neighborhoods: Harbourfront and Regent Park. These two rows will be combined into one row with the neighborhoods separated with a comma as shown in row 11 in the above table.
#   * If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough.
# 

# In[2]:


import pandas as pd
import requests
from bs4 import BeautifulSoup


# In[3]:


website_text = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
soup = BeautifulSoup(website_text,'xml')
table = soup.find('table',{'class':'wikitable sortable'})


# In[5]:


table_rows = table.find_all('tr')
data = []
for row in table_rows:
    td=[]
    for t in row.find_all('td'):
        td.append(t.text.strip())
    data.append(td)
df = pd.DataFrame(data, columns=['PostalCode', 'Borough', 'Neighborhood'])


# In[6]:


df = df[~df['Borough'].isnull()]  # to filter out bad rows
df.drop(df[df.Borough == 'Not assigned'].index, inplace=True)
df.reset_index(drop=True, inplace=True)
df = df.groupby(['PostalCode','Borough'])['Neighborhood'].apply(lambda x: ','.join(x)).reset_index()
df['Neighborhood'].replace('Not assigned',df['Borough'],inplace=True)
df


# In[7]:


df.shape


# ### Now that I have built a dataframe of the postal code of each neighborhood along with the borough name and neighborhood name, in order to utilize the Foursquare location data, I need to get the latitude and the longitude coordinates of each neighborhood and merge the data into one table. 

# In[9]:


df_geo_coordinate = pd.read_csv('http://cocl.us/Geospatial_data')
df_geo_coordinate.head()


# In[10]:


df_geo_coordinate.shape


# In[11]:


df_geo_coordinate.rename(columns={'Postal Code':'PostalCode'},inplace=True)
df_geo_coordinate.head()


# In[13]:


df.head()


# In[14]:


df_merged = df.join(df_geo_coordinate.set_index('PostalCode'), on='PostalCode')
df_merged


# In[20]:


get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes ')
import folium


# In[ ]:


get_ipython().system('conda install -c conda-forge geopy --yes')
from geopy.geocoders import Nominatim


# In[18]:



address = 'Toronto, ON'

geolocator = Nominatim(user_agent="t_explorer")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
# create map of New York using latitude and longitude values
map_t = folium.Map(location=[latitude, longitude], zoom_start=10)

# add markers to map
for lat, lng, borough, neighborhood in zip(df_merged['Latitude'], df_merged['Longitude'], df_merged['Borough'], df_merged['Neighborhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_newyork)  
    
map_t


# In[ ]:





# In[ ]:





# In[ ]:




