import requests
from bs4 import BeautifulSoup


class LiveMintScrapper:

    def extract(self,URL):
        #URL = "https://www.livemint.com/market/stock-market-news/chandrayaan-3-moon-landing-paras-defence-share-price-jumps-over-17-to-hit-a-fresh-52-week-high-11692850429978.html"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        main_area = soup.find('div', class_='mainArea', id='mainArea')
        if main_area:
            filtered_paragraphs = [p.text for p in main_area.find_all('p') if p.find('i') is None and p.find('a') is None]
            description = ' '.join(filtered_paragraphs)
            
            return description



class ScrapperFactory:
    def create_and_scrape(self, url):
        scraper = self.create_scraper(url)
        if not scraper:
            return None
        return scraper.extract(url)

    def create_scraper(self,url):
        if "livemint" in url:
            print('extracting from livemint')
            return LiveMintScrapper()
        else:
            return None

factory = ScrapperFactory()

