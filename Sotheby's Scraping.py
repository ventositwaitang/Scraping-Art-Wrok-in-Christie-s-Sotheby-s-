import requests
import csv
import json
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

#def pagenum():

count = 1
last_count = count
target = ['claude', 'monet',
          'pierre-auguste', 'renoir',
          'edgar', 'degas',
          'edouard', 'manet',
          'mary', 'cassatt',
          'camille','pissarro',
          'berthe','morisot',
          'joaquin','sorolla',
          'alfred','sisley',
          'max','liebermann']

first_name,surname = target[6],target[7]

def noNull(str):
    if len(str) != 0 or '|' in str:
        return str
    else:
        return ['']

with open(f"Art index_Sotheby's-{first_name}_{surname}.csv", 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["",'Artist name', 'Title of Artwork', 'Artwork type', 'Auction Location', 'Closed date',
                     'Currency', 'low Estimate', 'high Estimate', 'Price realised', 'Creation method', 'Size', 'Creation date', 'Website link'])
    # count = last_count
    json_data = {"requests": [{"indexName": "bsp_dotcom_prod_en",
                               "params": f"highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&hitsPerPage=51&filters=type%3A%22Bid%22%20OR%20type%3A%22Buy%20Now%22%20OR%20type%3A%22Lot%22%20OR%20type%3A%22Private%20Sale%22%20OR%20type%3A%22Retail%22&query={first_name}%20{surname}&maxValuesPerFacet=9999&page=1&facets=%5B%22type%22%2C%22endDate%22%2C%22lowEstimate%22%2C%22highEstimate%22%2C%22artists%22%5D&tagFilters=&facetFilters=%5B%5B%22type%3ALot%22%5D%5D"},
                              {"indexName": "bsp_dotcom_prod_en",
                               "params": f"highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=false&hitsPerPage=1&filters=type%3A%22Bid%22%20OR%20type%3A%22Buy%20Now%22%20OR%20type%3A%22Lot%22%20OR%20type%3A%22Private%20Sale%22%20OR%20type%3A%22Retail%22&query={first_name}%20{surname}&maxValuesPerFacet=9999&page=1&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&facets=type"}]}
    page = requests.post(
        "https://o28sy4q7wu-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia for JavaScript (4.2.0); Browser (lite); react (16.13.1); react-instantsearch (6.7.0); JS Helper (3.2.2)&x-algolia-api-key=e732e65c70ebf8b51d4e2f922b536496&x-algolia-application-id=O28SY4Q7WU",
        json=json_data)
    last_page_num = page.json()['results'][0]['nbPages']

    for num in range(1,last_page_num+1):
        json_data = {"requests": [{"indexName": "bsp_dotcom_prod_en",
                                "params": f"highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=true&hitsPerPage=51&filters=type%3A%22Bid%22%20OR%20type%3A%22Buy%20Now%22%20OR%20type%3A%22Lot%22%20OR%20type%3A%22Private%20Sale%22%20OR%20type%3A%22Retail%22&query={first_name}%20{surname}&maxValuesPerFacet=9999&page={num-1}&facets=%5B%22type%22%2C%22endDate%22%2C%22lowEstimate%22%2C%22highEstimate%22%2C%22artists%22%5D&tagFilters=&facetFilters=%5B%5B%22type%3ALot%22%5D%5D"},
                                {"indexName": "bsp_dotcom_prod_en",
                                "params": f"highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&clickAnalytics=false&hitsPerPage=1&filters=type%3A%22Bid%22%20OR%20type%3A%22Buy%20Now%22%20OR%20type%3A%22Lot%22%20OR%20type%3A%22Private%20Sale%22%20OR%20type%3A%22Retail%22&query={first_name}%20{surname}&maxValuesPerFacet=9999&page={num-1}&attributesToRetrieve=%5B%5D&attributesToHighlight=%5B%5D&attributesToSnippet=%5B%5D&tagFilters=&analytics=false&facets=type"}]}
        page = requests.post(
            "https://o28sy4q7wu-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia for JavaScript (4.2.0); Browser (lite); react (16.13.1); react-instantsearch (6.7.0); JS Helper (3.2.2)&x-algolia-api-key=e732e65c70ebf8b51d4e2f922b536496&x-algolia-application-id=O28SY4Q7WU",
            json=json_data)

        data = page.json()

    #'Artistic style',, data['filter']["label_txt"]
        for item in data['results'][0]['hits']:
            #print(target[4], item["artists"][0].split()[0].lower())
            if (len(item["artists"]) != 0 and first_name in item["artists"][0].split()[0].lower()) or (len(item["artists"]) != 0 and surname in item["artists"][0].split()[0].lower()):#if not in
                print(item['url'])
                try:

                    if item["auctionDetails"] is None:
                        auctionDetails = ' '
                    else:
                        auctionDetails = item["auctionDetails"].split('|')[0]
                    writer.writerow([
                        count, item["artists"][0].upper(), item["title"], item["departments"][0],
                        noNull(item["locations"])[0] + "|Sotheby's",
                        auctionDetails, item["estimateCurrency"], item["lowEstimate"], item["highEstimate"],
                        item["salePrice"], item["url"]])
                    print('added ', count, ' item ')
                    count += 1
                    last_count = count

                except Exception as e:
                    print(e)
        print('Page ',num,' done.')
