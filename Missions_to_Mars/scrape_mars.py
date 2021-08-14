import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
from webdriver_manager.chrome import ChromeDriverManager 

def scrape_news():
    # init browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news = {}

    #most recent article with teaser paragraph
    news["title"] = soup.select("div.content_title")[0].text
    news["body"] = soup.select("div.article_teaser_body")[0].text

    browser.quit()
    return (news)

def scrape_image():
    # init browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # featured image
    featured_image = browser.links.find_by_partial_href('featured')
    featured_image_url = featured_image["href"]

    browser.quit()
    return (featured_image_url)

def scrape_facts():
    # init browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://galaxyfacts-mars.com/' 
    tables = pd.read_html(url)
    tables[0]
    mars_facts = pd.DataFrame(tables[0])
    facts_noheader = mars_facts.rename(columns=mars_facts.iloc[0]).drop(mars_facts.index[0])
    html_table = facts_noheader.to_html()
    # html_cleaned = html_table.replace('\n', '') 

    browser.quit()
    return (html_table)

def scrape_hemis():
    # init browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    base_url = "https://marshemispheres.com/"
    browser.visit(base_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

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

        # dictionary containing Mars hemisphere images and titles (x4)
        hemisphere_image_urls.append({"title": title, "img_url": img_url})
        
    browser.quit()
    return (hemisphere_image_urls)


