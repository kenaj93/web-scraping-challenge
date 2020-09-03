from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    mars_dict = {}

    # news url
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")

    # Get article title and paragraph text(get code from JN)
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text

    # Images JN
    # Visit url 
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    # Go to 'FULL IMAGE'
    full_image = browser.links.find_by_partial_text('FULL IMAGE')
    full_image.click()
    time.sleep(5)

    # Go to 'more info'
    more_info = browser.links.find_by_partial_text('more info')
    more_info.click()

    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Scrape the URL
    image = soup.find('figure', class_='lede').a['href']
    featured_image = f'https://www.jpl.nasa.gov{image}'

    #Mars Facts
    # Visit Mars Facts 
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    html = browser.html

    # Use Pandas to scrape the table containing facts about Mars
    df = pd.read_html(facts_url)
    mars_facts = df[0]

    # Use Pandas to convert the data to a HTML table string
    mars_facts = mars_facts.to_html(classes="table table-striped")

    #hemispheres
    spheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(spheres_url)
    html_spheres = browser.html

    # Parse HTML 
    soup = BeautifulSoup(html_spheres, 'html.parser')

    # Retreive items that contain info
    items = soup.find_all('div', class_='item')

    # Create list for hemisphere urls 
    spheres_urls = []

    # Store the main_ul 
    main_url = 'https://astrogeology.usgs.gov'

    # Loop 
    for i in items: 
        title = i.find('h3').text
        image_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(main_url + image_url)
        image_html = browser.html 
        soup = BeautifulSoup(image_html, 'html.parser')
        image_url = main_url + soup.find('img', class_='wide-image')['src']
        spheres_urls.append({"title" : title, "image_url" : image_url})
    

# Display hemisphere_image_urls







    avg_temps = soup.find('div', id='weather')

    # Get the min avg temp
    min_temp = avg_temps.find_all('strong')[0].text

    # Get the max avg temp
    max_temp = avg_temps.find_all('strong')[1].text

    # BONUS: Find the src for the sloth image
    relative_image_path = soup.find_all('img')[2]["src"]
    sloth_img = url + relative_image_path

    # Store data in a dictionary
    costa_data = {
        "sloth_img": sloth_img,
        "min_temp": min_temp,
        "max_temp": max_temp
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return costa_data
