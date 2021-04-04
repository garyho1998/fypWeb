import json
import os  # file management
import re
from sys import platform  # check OS
from urllib.parse import SplitResult, urljoin, urlparse, urlsplit

import nltk
import pandas as pd
import requests
from bs4 import BeautifulSoup
from joblib import Parallel, delayed
from selenium import common, webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from boilerpipe.extract import Extractor


class RecursiveScraper:
    ''' Scrape URLs in a recursive manner.
    '''
    def __init__(self, maxWords, maxNode):
        ''' Constructor to initialize domain name and main URL.
        '''
        self.mainContents = ""
        self.maxWords = maxWords
        self.countWords = 0
        self.urlQueue = []
        self.maxNode = maxNode
        self.mainContent_dict = {}
        self.browser = self.brower_init()
        self.visited = {}

    def brower_init(self):
        options = webdriver.ChromeOptions()
        options.headless = False
        prefs = {'profile.default_content_setting_values': { 'images': 2, 'plugins': 2, 'popups': 2, 'geolocation': 2, 
                                    'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
                                    'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
                                    'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
                                    'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
                                    'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
                                    'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
                                    'durable_storage': 2}}
        options.add_experimental_option('prefs', prefs)
        options.add_argument("--enable-javascript")
        options.add_argument("--window-size=600,600")
        options.add_argument("--lang=en")
        options.add_argument('log-level=3')
        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        # options.add_argument("--headless")
        if platform == "win32": # if window
            browser = webdriver.Chrome('WebScraping/WebScraping_test_v1/chromedriver_win_88.exe',options=options)
        else: # Mac OS
            browser = webdriver.Chrome('./chromedriver',options=options)
        return browser

    def preprocess_url(self, referrer, url):
        ''' Clean and filter URLs before scraping.
        '''
        if not url:
            return None
        ref_urlparse = urlparse(referrer)
        base = (ref_urlparse.scheme if ref_urlparse.scheme else "http") + "://" + ref_urlparse.netloc+ref_urlparse.path

        fields = urlparse(urljoin(base, url)) # convert to absolute URLs and split
        if fields.netloc == self.domain:
            if fields.geturl() not in self.urlQueue and fields.geturl() not in self.visited:
                return fields.geturl()
        return None

    def scrapeBFS(self, mainurl):
        self.domain = urlsplit(mainurl).netloc

        num_visited_node = 0
        num_words = 0
        
        self.urlQueue.append(mainurl)
        self.visited[mainurl] = True

        while self.urlQueue and num_visited_node<self.maxNode and num_words<self.maxWords:
            url = self.urlQueue.pop(0)
            num_visited_node += 1
            try:
                self.browser.get(url)
                if(url==mainurl):
                    element_present = EC.presence_of_element_located((By.TAG_NAME, 'body'))
                    WebDriverWait(self.browser, 3).until(element_present)

                soup = BeautifulSoup(self.browser.page_source, 'lxml')
            
                content = self.getTokenizedMainContents(self.browser.page_source)
                num_words += len(content)
                self.mainContent_dict[self.browser.current_url] = content

                for link in soup.findAll("a"):
                    childurl = self.preprocess_url(self.browser.current_url, link.get("href"))
                    if childurl and childurl not in self.visited:
                        if("blog" not in childurl and "blog-list" not in childurl and "product-list" not in childurl 
                            and "mailto:" not in childurl and "news" not in childurl
                            and "/zh" not in childurl and "lang=ZH" not in childurl 
                            and "/sc" not in childurl and "lang=SC" not in childurl
                            and "/cn" not in childurl and "lang=CN" not in childurl  
                            and "/tc" not in childurl and "lang=TC" not in childurl):
                            print("         childurl", childurl)
                            self.urlQueue.append(childurl)
                        self.visited[childurl] = True
            except Exception as e:
                print("scrapeBFS(): ", e)

        self.mainContent_dict["num_visited_node"] = num_visited_node            
        self.mainContent_dict["num_words"] = num_words
        print("finish ", mainurl)
        self.browser.close()
    
    def getTokenizedMainContents(self,page_source):
        if page_source is None:
            return ""
        try:
            extractor = Extractor(extractor='ArticleExtractor', html=page_source, kMin=20, output='json')
        except:
            print("extract error")
            return ""
        extracted_text = extractor.getText()
        return str(extracted_text)

    
    def tokenizeText(self, text):
        sent_text = nltk.sent_tokenize(text) # this gives us a list of sentences
        # now loop over each sentence and tokenize it separately
        texts = []
        for sentence in sent_text:
            tokenized_text = nltk.word_tokenize(sentence)
            # tagged = nltk.pos_tag(tokenized_text)
            texts += [x for x in tokenized_text if len(x) > 1]
        return len(texts)


def formaturl(url):
    urls = url.replace(" ", "").split(",")
    return [((urlparse(x).scheme if urlparse(x).scheme else 'http') + '://' + urlparse(x).netloc + urlparse(x).path).replace(" ", "") for x in urls ]

def start(url):
    try:
        df_urls = formaturl(url)
        if not df_urls:
            return None
        for url in df_urls:
            fileName = "WebScraping/scraping_data_json/" + urlparse(url).netloc.replace('www.','').replace('/','-').replace(":","_").replace('.','-') + "_test.txt"     
            
            if os.path.isfile(fileName):
                # print(fileName, "exist.")
                return None

            print("website", url)
            rscraper = RecursiveScraper(maxWords=500000, maxNode=300)
            rscraper.scrapeBFS(mainurl = url)
            
            with open(fileName, "w", encoding="utf-8") as f:
                f.write(json.dumps(rscraper.mainContent_dict))
    except Exception as e:
        print("start(): ", e)
    
if __name__ == '__main__':
    list_it_df = pd.read_excel("WebScraping/WebScraping_test_v1/list_it_solutions.xlsx", sheet_name=0, engine='openpyxl')
    list_it_df = list_it_df.dropna(subset=['Website'])
    website_list = list_it_df['Website'].drop_duplicates().tolist()
    Parallel(n_jobs=6)(delayed(start)(url) for url in website_list)
