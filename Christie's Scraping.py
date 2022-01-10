import requests
import csv
import json
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
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

first_name,surname = target[6],target[7] # Changing your target artist here #

def noOut5(lst):
    for i in range(5-len(lst)):
        lst.append(' ')
    return lst

with open(f"Art index_Christie's-{first_name}_{surname}.csv", 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["",'Artist name', 'Title of artwork', 'Auction location', 'Closed date',
                     'Currency', 'Low estimate', 'High estimate', 'Price realised',
                     'Signature and Creation method', 'Size', 'Creating year', 'Website link'])
    #count = last_count
    page = requests.get(f"https://www.christies.com/api/discoverywebsite/search/lot-infos?keyword={first_name}%20{surname}&page=1&is_past_lots=true&language=en")
    last_page_num = page.json()['total_pages']

    for num in range(1,last_page_num+1):
        page = requests.get(f"https://www.christies.com/api/discoverywebsite/search/lot-infos?keyword={first_name}%20{surname}&page={num}&is_past_lots=true&language=en")
        data = page.json()
        #'artistic style',, data['filter']["label_txt"]

        for item in data['lots']:
            print(item["title_primary_txt"].lower().startswith(first_name))
            if item["title_primary_txt"].lower().startswith(first_name) or item["title_primary_txt"].lower().startswith(surname): #if not in
                print(item['url'])
                try:
                    tag = item['url']
                    req = Request(tag, headers={'User-Agent': 'Mozilla/5.0'})
                    tag_page = urlopen(req).read()
                    soup = BeautifulSoup(tag_page, 'html.parser')
                    try:
                        span = soup.find('span',class_="chr-lot-section__accordion--text")#.find('chr-accordion-item',{'accordion-id':'0'}).
                        #print(span)
                        elms = noOut5(list(filter(None, span.get_text().split('\n'))))#.replace('\n',',')
                        #print(elms)
                        #print('Title of Artwork: ',elms[1],'|Signature: ', elms[2],'|Creation method:', elms[3],'|Size:',elms[4], '|Creation year:', elms[5][-4:])
                        ##pattern = re.compile(r"window.chrComponents.carousel_677142815 = '(.*?)';$", re.MULTILINE | re.DOTALL)
                        ##script = soup.html.find('script',text=pattern)#[17].contents
                        #script = soup.html.find_all('script')[16]#.c vontents
                        #for script_posi in soup.html.find_all('script'):
                            #print(script_posi)
                            #if "window.chrComponents.lotHeader_1205114186" in script_posi: ######
                                #print(type(script_posi))
                                #print(soup.html.find_all('script').index(script_posi))
                                #script = soup.html.find_all('script')[soup.html.find_all('script').index(script_posi)]
                        script = soup.find('script',text = re.compile('window.chrComponents.lotHeader_1205114186 ='))
                        match = re.search(r'window.chrComponents.lotHeader_1205114186 = {.+?};', str(script))
                        string = match.group(0).replace("window.chrComponents.lotHeader_1205114186 = ", "")[:-1]
                        tag_data = json.loads(string)['data']
                        #print(tag_data['sale']['location_txt'])
                        # tag_string = re.search(r'{"data":{.+},',string).group(0)[:-1]
                        # tag_tag_string= re.search(r'{"sale":{.+},',tag_string)#.group(0)[:-1]
                        ##print(pattern.search(script.text).group(1)

                        if elms[-1].split(' in ')[-1] is None:
                            Creating_year = ' '
                        else:
                            Creating_year = elms[-1].split(' in ')[-1]
                        if tag_data['sale']['location_txt'] is None:
                           location = ' '
                        else:
                            location = tag_data['sale']['location_txt']
                        #-------#
                        sign_meth = '--'.join((elms[2]+'--'+elms[-3]).split('--')[:2])
                        #-------#

                        writer.writerow([count, item["title_primary_txt"].upper(), elms[1], location + "| Christie's"
                            ,item["end_date"], item["price_realised_txt"][:3], tag_data['lots'][0]['estimate_low'],tag_data['lots'][0]['estimate_high'],item["price_realised_txt"][3:]
                            , sign_meth, elms[-2], Creating_year, item["url"]])

                        print('added ', count, ' item ')
                        count += 1
                        last_count = count
                    except Exception as e:
                        print(e)
                        continue
                except Exception as e:
                    print(e)
                    continue
        print('Page ',num,' done.')


### columns: Matterial, Size, Creation date, creation method
# print(soup.prettify().encode('ascii', 'ignore'))
