#Declare Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

def init_browser():
    executable_path = {'executable_path' : 'C:/Users/mendi/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_data = {}
    
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    # URL of page to be scraped

    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(2)   

    # Retrieve page with the requests module
    html = browser.html
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find('div', class_='content_title').find('a').text

        # Identify and return price of listing
    news_p = soup.find('div', class_='article_teaser_body').text

    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p

    #JPL Mars Space Images
    mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_image_url)
    time.sleep(1)

    image_html = browser.html

    #Parse HTML with Beautiful Soup
    image_soup = BeautifulSoup(image_html, 'html.parser')

    #find first Mars image url  
    img_path = image_soup.find('img', class_='thumb')['src']

    #combine url to get image path
    featured_image_url = f'https://www.jpl.nasa.gov{img_path}'

    mars_data['featured_image_url'] = featured_image_url

    #Mars Weather

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(1)
    weather_tweet = browser.html

    #Parse HTML with Beautiful Soup
    weather_soup = BeautifulSoup(weather_tweet, 'html.parser')

    tweets = weather_soup.find('ol', class_='stream-items')
    mars_weather = tweets.find('p', class_="tweet-text").text

    mars_data['weather_summary'] = mars_weather

    #Mars Facts
    mars_facts_url = 'https://space-facts.com/mars/'
    browser.visit(mars_facts_url)
    mars_facts = browser.html

    #Parse HTML with Beautiful Soup
    mars_facts_soup = BeautifulSoup(mars_facts, 'html.parser')

    fact_table = mars_facts_soup.find('table', class_='tablepress tablepress-id-mars')
    column1 = fact_table.find_all('td', class_='column-1')
    column2 = fact_table.find_all('td', class_='column-2')

    descriptions = []
    values = []

    for row in column1:
        description = row.text.strip()
        descriptions.append(description)
        
    for row in column2:
        value = row.text.strip()
        values.append(value)
        
    mars_facts = pd.DataFrame({
        "Description":descriptions,
        "Value":values
        })

    mars_facts_html = mars_facts.to_html(header=False, index=False)

    mars_data['mars_facts'] = mars_facts_html

    #Mars Hemispheres
    mars_hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres_url)
    time.sleep(1)

    #HTML object
    hemisphere_html = browser.html

    #Parse HTML with Beautiful Soup
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')

    #Retreive all items that contain mars hemispheres information
    items = hemisphere_soup.find_all('div', class_='item')

    #Create an empty list for hemisphere urls
    hemisphere_image_urls = []

    #store the main url
    main_hemisphere_url = 'https://astrogeology.usgs.gov'

    #loop through items stored
    for i in items:
        #store title
        title = i.find('h3').text


        #store the link to image
        image_url = i.find('a', class_='itemLink product-item')['href']

        #visit the link for the full image website
        browser.visit(main_hemisphere_url + image_url)
    
        #HTML object for individual hemisphere sites
        image_url = browser.html    
    
        #Parse HTML with Beautiful Soup for each hemisphere
        image_soup = BeautifulSoup(image_url, 'html.parser')
    
        #image pate
        hemisphere_img_path = image_soup.find('img', class_='wide-image')['src']
    
        #retrieve full image source
        full_img_url = f'https://astrogeology.usgs.gov{hemisphere_img_path}'
    
        #append title and urls to list
        hemisphere_image_urls.append({
            "title": title,
            "full_image_url": full_img_url
        })

        mars_data['hemisphere_imgs'] = hemisphere_image_urls
    
    browser.quit()

    return mars_data

#print(scrape())
#print(hemisphere_img_path)