import requests
from bs4 import BeautifulSoup
import pandas as pd 

print('')
CSV_fileName = input('Enter a product to search for: ')

searchTerm = CSV_fileName.replace(' ', '+')

def get_data(searchTerm):
    url = "https://www.ebay.com/sch/i.html?LH_PrefLoc=3&LH_TitleDesc=0&_fsrp=1&LH_Auction=1&_sacat=0&_nkw=" + searchTerm + "&_from=R40&LH_Sold=1&rt=nc&_oaa=1&_dcat=139971"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productsList = []
    results = soup.findAll('div', {'class': 's-item__info clearfix'})
    for item in results:
        product = {
            'title': item.find('h3', {'class': 's-item__title s-item__title--has-tags'}).text,
            'soldprice': float(item.find('span', {'class': 's-item__price'}).text.replace('$','').replace(',','').strip()),
            'solddate': item.find('span', {'class': 's-item__ended-date s-item__endedDate'}).text,
            'bids': item.find('span', {'class': 's-item__bids'}).text,
            'link': item.find('a', {'class': 's-item__link'})['href'],
        }
        productsList.append(product)
    return productsList

def output(productsList):
    productsDF = pd.DataFrame(productsList)
    productsDF.to_csv( 'ebay_price_scraper/data/' + CSV_fileName + ' - Past_Auctions.csv', index=False)
    print('Saved to CSV')
    return

soup = get_data(searchTerm)
productsList = parse(soup)
output(productsList)

print('Program Complete')