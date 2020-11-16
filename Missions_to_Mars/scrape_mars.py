# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from pprint import pprint
import warnings
warnings.filterwarnings("ignore")

def init_browser():
    executable_path = {"executable_path": "C:/temp/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
  browser = init_browser()

  # Visit the NASA Mars News Site
  url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
  browser.visit(url)
  # Wait for page elements to load
  time.sleep(1)
  
  # Scrape page into soup.
  html = browser.html
  soup = bs(html, "html.parser")
  # Get latest news title and paragraph text
  news_title = soup.find_all('div', class_='content_title')[1].text
  news_p = soup.find_all('div', class_="article_teaser_body")[0].text
  print(news_title)
  print(news_p)

  # Visit the Jet Propulsion Laboratory website for the Featured Space Image
  url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
  browser.visit(url)

  # Wait for page elements to load
  time.sleep(1)

  # Scrape page into soup
  html = browser.html
  soup = bs(html, "html.parser")

  # Get image url for featured image
  results = soup.find("article")
  featured_image_base_url = "https://www.jpl.nasa.gov"
  featured_image_url = featured_image_base_url + results["style"].split("'")[1]
  print(featured_image_url)

  # Visit url for mars facts
  url = "https://space-facts.com/mars/"
  browser.visit(url)

  # Wait for page/page elements to load
  time.sleep(1)

  # Scrape page into soup
  html = browser.html
  soup = bs(html, "html.parser")

  # Get Mars facts table using pandas
  tables = pd.read_html(url)
  tables

  # Convert table for site to dataframe
  mars_profile_df = tables[0]
  mars_profile_df.columns = ["Measurement", "Value"]
  mars_profile_df.set_index("Measurement", inplace=True)
  mars_profile_df.head()

  # Convert dataframe to html string
  mars_profile_html = mars_profile_df.to_html()
  mars_profile_html

  # Remove new line characters from html string
  mars_profile_html.replace("\n", "")

  # Export html string
  mars_profile_df.to_html("Resources/mars_planet_profile_table.html")

  # Visit Astrogeology url
  url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
  browser.visit(url)

  # Wait for page elements to load
  time.sleep(1)

  # Scrape page into soup
  html = browser.html
  soup = bs(html, "html.parser")

  # Get hemisphere name and image url for the full resolution image
  hemispheres = soup.find_all('div', class_='item')
  hemisphere_image_urls = []

  for hemisphere in hemispheres:
      link_text = hemisphere.find("h3").text
      splitted = link_text.split("Enhanced")
      title = splitted[0]
      browser.click_link_by_partial_text(link_text)
      hemisphere_page_html = browser.html
      soup = bs(hemisphere_page_html, "html.parser")
      downloads = soup.find('div', class_="downloads")
      img_url = downloads.a["href"]
      hemisphere_dict = { "title": title, "img_url": img_url }
      hemisphere_image_urls.append(hemisphere_dict)
      browser.back()
    
  pprint(hemisphere_image_urls)

  scraped_data = {
    "news_title": news_title,
    "news_p": news_p,
    "hemisphere_image_urls": hemisphere_image_urls,
    "mars_profile_html": mars_profile_html,
    "featured_image_url": featured_image_url
  }

  print(scraped_data)

  # Close the browser after scraping
  browser.quit()

  # Return results  
  return scraped_data