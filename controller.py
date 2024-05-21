import asyncio
from crawler import Crawler
from preprocessor import Preprocessor   

class Controller:
    def __init__(self):
        self.crawler = Crawler()
        self.preprocessor = Preprocessor()
        self.email = "seonu2001@kookmin.ac.kr"
        self.latest_id = '527'

    def get_notice(self, keyword=None, article_id=None, lang='ko'):
        notice_url, title, image_urls = self.crawler.scrape_notice(keyword, article_id)
        if title == "":
            notice = self.preprocessor.make_notice(notice_url, title, image_urls, lang=lang)
            return notice
        else:
            return "No notices found."

    async def new_notice(self):
        hp_latest_id = self.crawler.get_latest_id()
        if(hp_latest_id != self.latest_id):
            self.latest_id = hp_latest_id
            return self.latest_id
        else:
            return -1

    def get_email(self):
        return self.email

async def main():
    controller = Controller()
    rst = await controller.get_notice('추가모집', None, 'ko')
    print(rst)

    # For testing new_notice functionality
    latest_notice = await controller.new_notice()
    print(latest_notice)

if __name__ == "__main__":
    asyncio.run(main())
