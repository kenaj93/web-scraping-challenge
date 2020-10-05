from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time


def scrape():
    # browser=init_browser()
    # return {
    #    'mars_news': mars_news(browser),
    #     'mars_featured_image': mars_image (browser),
    #     'mars_facts':mars_facts(),
    #     'mars_hemispheres': mars_hemispheres (browser)
    # }

    return {"mars_news"}
def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    
    news_titles = {}    
    url='https://mars.nasa.gov/news/'
    # browser = init_browser()
    time.sleep(2)
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    news_title= soup.find('div', class_= 'content_title').text
    news_p =soup.find ('div', class_='article_teaser_body').text
  
    # Dictionary Entry from Mars Info News
    news_titles['news_title']= news_title
    news_titles['news_paragraph']=news_p

    return news_titles

#calling the function
# news_titles= scrape()


def mars_image(browser):
    full_image = {}
    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit (url)

    image_full=browser.find_by_id('full_image')
    image_full.click()
    time.sleep(2)
    browser.click_link_by_partial_text('more info')

    html_image = browser.html
    soup = BeautifulSoup(html_image, 'html.parser')

    img_url=soup.find('img', class_ = 'main_image')['src']
    featured_image = "https://www.jpl.nasa.gov" + img_url

    full_image ['featured_image'] = featured_image
    # browser.quit()
    return full_image 





# Mars Facts 
def mars_facts():
    # mars_facts ={}
    #Use Pandas to read table
    facts_df =pd.read_html('https://space-facts.com/mars/')[1]
    # facts_df
    #Find Mars facts DataFrame
    facts_df.columns=["Description","Values"]
    # facts_df
    # DataFrames as HTML
    #Generate HTML tables from DataFrame using Pandas and set column headers with description and value
    facts_df=facts_df.to_html()
    # facts_df

# Dictionary Entry from Mars Facts 
    # mars_facts['facts_df'] = facts_df

    return facts_df
    # Close the browser after scraping
  


# Mars Hemispheres 
def mars_hemispheres(browser):
    mars_news = {}
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # browser = init_browser ()
    browser.visit (url)
    #Parse with 'html.parser';creation with beautifulsoup object
    html_hemispheres = browser.html
    soup = BeautifulSoup(html_hemispheres , 'html.parser')

    #Create an empty list of links for the hemispheres
    hemisphere_image_urls=[]
    products=soup.find ('div', class_='result-list')
    hemispheres=products.find_all('div',{'class':'item'})

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html_hemispheres = browser.html
        soup=BeautifulSoup(html_hemispheres, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})


    #Display hemisphere image urls
    hemisphere_image_urls

    # Dictionary Entry from Mars Hemispheres 
    mars_news ['hemisphere_image_urls']= hemisphere_image_urls


    return  hemisphere_image_urls