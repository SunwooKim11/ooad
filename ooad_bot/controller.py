from crawler import Crawler
from preprocessor import Preprocessor   

class Controller:
    def __init__(self):
        self.crawler = Crawler()
        self.preprocessor = Preprocessor()
        self.email = "seonu2001@kookmin.ac.kr"
        self.latest_id = '527'

    async def get_notice(self, keyword=None, id=None, lang='ko'):
        matching_notice = await self.crawler.scrape_notice(keyword, id) #keyword와 id를 가지고 이미지 scrape
        if matching_notice:
            processed_notice = await self.preprocessor.preprocess_content(matching_notice, lang='ko')  #img를 가지고 텍스트 뽑아내기
            return processed_notice
        else:
            return "No notices found."
        
    async def new_notice(self): # page의 첫번재 id를 얻어 공지사항이 최신인지 확인
        hp_latest_id = self.crawler.get_latest_id()
        if(hp_latest_id!= self.latest_id):
            self.latest_id = hp_latest_id
            return self.latest_id
        else:
            return -1

    def get_email(self):
        return self.email