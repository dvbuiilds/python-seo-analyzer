import sys
import random
from robobrowser import RoboBrowser
import datetime
import csv
import time
import requests
import json


#Mobile user agent strings found on https://deviceatlas.com/blog/mobile-browser-user-agent-strings
mobile_agent = [
    #Safari for iOS
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
    #Android Browser
    'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    #Chrome Mobile
    'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
    #Firefox for Android
    'Mozilla/5.0 (Android 7.0; Mobile; rv:54.0) Gecko/54.0 Firefox/54.0',
    #Firefox for iOS
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) FxiOS/7.5b3349 Mobile/14F89 Safari/603.2.4',
    #Samsung Browser
    'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G955U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
]

# desktop user agent strings. Source: https://deviceatlas.com/blog/list-of-user-agent-strings
desktop_agent = [
    ## Chrome 60 Windows
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    ## Firefox 36 Windows
    'Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0',
    ### Chrome 67 Windows
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    ### Chrome 79 Windows 
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    ### Webkit MacOs
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko)',
    ### Chrome 79 MacOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    ## FireFox Generic MacOS
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:54.0) Gecko/20100101 Firefox/54.0'
]

def get_page_load_speed(url, device):
    if url[:4] != "http":
        url = "https://" + url
    start_time = time.time() 
    user_agent = random.choice(desktop_agent) if device == "desktop" else random.choice(mobile_agent)
    requests.get(url, headers={"Content-Type":"text", "User-agent": user_agent}) 
    end_time = time.time() 
    load_time = end_time - start_time 
    return load_time

def get_page_rank(website, keyword, device):
    url = "https://www.google.com"
    user_agent = random.choice(desktop_agent) if device == "desktop" else random.choice(mobile_agent)
    browser = RoboBrowser(history=False, user_agent=user_agent, parser='html.parser')
    page_url = 'https://www.google.com/search?q=' + keyword+"&start="
    browser.open(page_url)
    print("browser opened!")

    tds = browser.find_all("td")
    tds = [td.get_text() for td in tds]
    if(not len(tds)):
        return -2
    print(tds)
    i = len(tds)-1
    final_page = 0
    while i >=0 :
        if(tds[i].isnumeric()):
            final_page = int(tds[i])
            break
        i -=1
    i = 0
    serp_links = list()
    while i<final_page*20:
        serp_links.append(page_url+str(i))
        i += 20

    rank = 0
    flag = False

    for serp in serp_links:
        # page_url = url + serp
        print("Page visited is : ", serp)

        browser.open(serp)
        cite_tags = browser.find_all("cite")
        cite_links = [tag.get_text() for tag in cite_tags]
        
        only_urls = []
        for link in cite_links:
            only_urls.append(link.split(' ')[0])
        cite_links = set(only_urls)

        for link in cite_links:
            if website in link:
                flag = True
                break
            else:
                rank += 1

        if flag:
            print("Website Ranked! ", rank+1)
            return rank

        time.sleep(10)

    return -1

def main():
    keywords = list()
    with open('keywords.csv', 'r') as file:
        my_reader = csv.reader(file, delimiter=',')
        for row in my_reader:
            keywords.append(row[0])

    sitename = sys.argv[1]
    device = sys.argv[2]

    load_speed = get_page_load_speed(sitename, device)
    key_rank_pair_arr = list()
    rank = -2

    for keyword in keywords:
        try:
            rank = get_page_rank(sitename, keyword, device)
        except requests.exceptions.ConnectionError:
            rank = -2

        if(rank == -1):
            rank = "site not ranked for this keyword."
        elif rank > -1:
            rank += 1
        else:
            rank = "server error."
        key_rank_pair_arr.append({"keyword": keyword, "rank": rank})
        time.sleep(10)

    response = {
        "device": device,
        "page_load_speed": load_speed,
        "keywords_result": key_rank_pair_arr
    }

    with open((datetime.date.today().strftime("%Y-%m-%d_%H-%M-%S")+'-' +keyword+".json"), "w") as json_file:
        json.dump(response, json_file)

main()