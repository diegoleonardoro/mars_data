from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd


def scrape():

    # setting up Selenium:

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path='/Users/diegoleoro/Downloads/chromedriver', options=chrome_options)

    # scraping news:

    mars_news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    driver.get(mars_news_url)
    pageSource_news = driver.page_source
    bs_news = BeautifulSoup(pageSource_news, "html.parser")
    news_title = bs_news.find_all('div', {'class': 'content_title'})
    news_title_text = [title.text.strip() for title in news_title]
    newsparagraph = bs_news.find_all('div', class_="article_teaser_body")
    newsparagraph_text = [news.text.strip() for news in newsparagraph]

    # getting images:

    mars_images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    driver.get(mars_images_url)
    pageSource_Images = driver.page_source
    bs_images = BeautifulSoup(pageSource_Images, 'html.parser')
    images = bs_images.find_all('img', {'class': 'thumb'})
    image_src = [i['src'] for i in images]
    images_url_parse = urlparse(mars_images_url)
    images_urls = [images_url_parse.scheme + "://" +
                   images_url_parse.netloc + i for i in image_src]

    # getting Twitter updates:

    mars_twitter_url = "https://twitter.com/marswxreport?lang=en"

    driver.get(mars_twitter_url)
    pageSource_Twitter = driver.page_source
    bs_twitter = BeautifulSoup(pageSource_Twitter, 'html.parser')
    tweets = bs_twitter.find_all(
        'p', {'class': 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text'})
    tweets_text = [t.text.strip() for t in tweets]

    # getting mars facts:

    url_mars_facts = "https://space-facts.com/mars/"
    table = pd.read_html(url_mars_facts)
    table = table[0]
    table_html = table.to_html()

    # getting hemispheres images:

    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    driver.get(mars_hemispheres_url)

    pageSouce_hemispheres = driver.page_source

    bs_hemispheres = BeautifulSoup(pageSouce_hemispheres, "html.parser")

    link_div = bs_hemispheres.find_all('div', {'class': 'description'})
    link = [l.a["href"] for l in link_div]
    images_url_parse = urlparse(mars_hemispheres_url)

    url_to_image = [images_url_parse.scheme + "://" +
                    images_url_parse.netloc + i for i in link]

    images_hemispheres_high_res = []
    hemisphere_name = []

    for url in url_to_image:
        driver.get(url)
        image_page_source = driver.page_source
        bs_image = BeautifulSoup(image_page_source, "html.parser")
        image_link = bs_image.find("a", {"target": "_blank"})
        image_href = image_link["href"]
        images_hemispheres_high_res.append(image_href)

        hemisphere = bs_image.find("h2", {"class": "title"}).text
        hemisphere_name.append(hemisphere)

    images_hemisphere_dict_list = []

    for i, e in zip(hemisphere_name, images_hemispheres_high_res):
        dict_ = {}
        dict_["Title"] = i
        dict_["Image_url"] = e
        images_hemisphere_dict_list.append(dict_)

    # dictionary:

    mars_data = {
        "news_title": news_title_text,
        "news_paragraph": newsparagraph_text,
        "tweets_text": tweets_text,
        "facts_table": table_html,
        "images_hemispheres": images_hemisphere_dict_list,
    }

    return mars_data
