from crawler import Crawler
from preprocessor import Preprocessor   

class Controller:
    def __init__(self):
        self.crawler = Crawler()
        self.preprocessor = Preprocessor()
        self.email = "seonu2001@kookmin.ac.kr"
        self.latest_id = '527'

    async def get_notice(self, keyword=None, id=None, lang='ko'):
        matching_notice = await self.crawler.scrape_notice(keyword, id)
        if matching_notice:
            processed_notice = await self.preprocessor.preprocess_content(matching_notice, lang='ko')
            return processed_notice
        else:
            return "No notices found."
    async def new_notice(self):
        hp_latest_id = self.crawler.get_latest_id()
        if(hp_latest_id!= self.latest_id):
            self.latest_id = hp_latest_id
            return self.latest_id
        else:
            return -1

    def get_email(self):
        return self.email