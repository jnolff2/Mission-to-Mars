# Imports
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from splinter import Browser


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    

def scrape():

    browser = init_browser()

    # Create dictionary to hold all of the scraped data
    mars_dictionary = {}


    # Create a variable for the NASA url
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    # Create a BeautifulSoup object and parse it
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # Collect the latest News Title and Paragraph Text from the NASA Mars News Site
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text

    mars_dictionary["news_title"] = news_title
    mars_dictionary["news_p"] = news_p


    # Visit the url for the JPL Featured Space image
    images_url ="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_url)
    # Find the image url for the current Featured Mars image and assign it to a variable
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # The image url was located in a css style tag with "backgroud-image: url('');" so I had to have the image remove the
    # first 23 characters and the last 3 characters in the string
    image = soup.find("article", class_="carousel_item")["style"]
    featured_image_url = "https://www.jpl.nasa.gov/" + image[23:-3]

    mars_dictionary["featured_image_url"] = featured_image_url
      

    # Create a variable to hold the Mars Weather Twitter page url
    mars_weather_url ="https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # Scrape the most recent tweet from the Mars Weather Twitter account
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    mars_dictionary["mars_weather"] = mars_weather
    

    # Create a variable for the Mars Facts url
    mars_facts_url= "https://space-facts.com/mars/"
    # Create a BeautifulSoup object and parse it
    response = requests.get(mars_facts_url)
    soup = BeautifulSoup(response.text, "html.parser")
    # Take the Mars-Earth comparison table from the url page, place it into a dataframe, and then convert it to an html table
    table = pd.read_html(mars_facts_url)
    mars_facts = pd.DataFrame(table[0])
    mars_facts.columns=["Data", "Mars", "Earth"]
    mars_df = mars_facts.set_index("Data")
    mars_table = mars_df.to_html(classes="mars_table")
    mars_table = mars_table.replace("\n", "")
    mars_dictionary["mars_table"] = mars_table


    # Create a variable for the USGS Astrogeology url
    mars_hemispheres_url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemispheres_url)
    # Create a BeautifulSoup object and parse it
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # Create a dictionary to hold the 4 hemisphere
    hemisphere_image_urls = []
    # Loop through the 4 different hemisphere images by clicking on each one and grabbing the image url and image title
    for i in range (4):
        images = browser.find_by_tag("h3")
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        image = soup.find("img", class_="wide-image")["src"]
        img_title = soup.find("h2", class_="title").text
        img_url = "https://astrogeology.usgs.gov" + image
        mars_dict = {"title": img_title, "img_url": img_url}
        hemisphere_image_urls.append(mars_dict)
        browser.back()

    mars_dictionary["hemisphere_image_urls"] = hemisphere_image_urls
    # Close the browser after scraping the page
    browser.quit()      


    return mars_dictionary