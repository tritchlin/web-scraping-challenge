# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
from webdriver_manager.chrome import ChromeDriverManager 

# %%
# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# %%
url = 'https://redplanetscience.com/'
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

# %%
latest_title = soup.select("div.content_title")[0].text
latest_news_p = soup.select("div.article_teaser_body")[0].text

# %%
url = "https://spaceimages-mars.com/"
browser.visit(url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

featured_image = browser.links.find_by_partial_href('featured')
featured_image_url = featured_image["href"]

# %%
url = 'https://galaxyfacts-mars.com/' 
tables = pd.read_html(url)
tables[1]
mars_facts = pd.DataFrame(tables[1])
html_table = mars_facts.to_html()
html_cleaned = html_table.replace('\n', '') 

# %%
base_url = "https://marshemispheres.com/"
browser.visit(base_url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

# %%
body = soup.body.find_all(class_='item')
hemisphere_image_urls = []

for item in body:
    product = item.a
    partial = product['href']
    subpage_link = base_url + partial

    browser.visit(subpage_link)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    desc = soup.find('dl')
    img_partial = desc.find('a')['href']

    title = soup.find('h2').get_text()
    img_url = base_url + img_partial

    hemisphere_image_urls.append({"title": title, "img_url": img_url})

print(hemisphere_image_urls)

# %%
browser.quit()


