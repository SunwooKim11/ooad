from crawler import Crawler
from preprocessor import Preprocessor   

class Controller:
    def __init__(self):
        self.crawler = Crawler()
        self.preprocessor = Preprocessor()

    async def get_notice(self, keyword=None, uri=None):
        matching_notice = await self.crawler.scrape_notice(keyword, uri)
        if matching_notice:
            processed_notice = await self.preprocessor.preprocess_content(matching_notice, translation=True)
            return processed_notice
        else:
            return "No notices found."