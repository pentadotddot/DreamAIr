# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 13:56:34 2023

@author: RUID
"""

from bs4 import BeautifulSoup
import requests

import replicate
import os

files = []
directory = r'F://AIDREAM//telex'

 #%%

html_page = requests.get('https://telex.hu/')
soup = BeautifulSoup(html_page.content, 'html.parser')
image_tags = soup.find_all('img')
image_tags=image_tags[1:11:]
links = []
for image_tag in image_tags:
    links.append(image_tag['src'])
    
links = links[1::]
 #%%soup = BeautifulSoup(response.content, 'html.parser')
for counter, image_tag in enumerate(image_tags):
    image_url = image_tag['src']
    response = requests.get(image_url)
    print(image_url, response.status_code)
    with open(str(counter) + '.jpg', 'wb') as f:
        for chunk in response.iter_content(chunk_size=128):
            f.write(chunk)

 #%%

# assign directory
files = []
directory = r'F://AIDREAM//telex'
 
# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        files.append(f)


records =[]



for i in files: 
    model = replicate.models.get("pharmapsychotic/clip-interrogator")
    version = model.versions.get("a4a8bafd6089e1716b06057c42b19378250d008b80fe87caa5cd36d40c1eda90")
    
    # https://replicate.com/pharmapsychotic/clip-interrogator/versions/a4a8bafd6089e1716b06057c42b19378250d008b80fe87caa5cd36d40c1eda90#input
    inputs = {
        # Input image
        'image': open(i, "rb"),
    
        # Choose ViT-L for Stable Diffusion 1, and ViT-H for Stable Diffusion
        # 2
        'clip_model_name': "ViT-H-14/laion2b_s32b_b79k",
    
        # Prompt mode (best takes 10-20 seconds, fast takes 1-2 seconds).
        'mode': "fast",
    }

# https://replicate.com/pharmapsychotic/clip-interrogator/versions/a4a8bafd6089e1716b06057c42b19378250d008b80fe87caa5cd36d40c1eda90#output-schema
    output = version.predict(**inputs)
    records.append(output)
    print(output)
    
    
  #%%
import pandas as pd
df = pd.DataFrame(records)
  #%%
df.set_axis(['word'], axis='columns', inplace=True)
  #%%
df2 =df.word.str.split(',',expand=True).add_prefix('word_')

  #%%
df2.to_excel("telex_0213.xlsx") 