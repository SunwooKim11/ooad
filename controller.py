import asyncio
from crawler import Crawler
from notice_creator import NoticeCreator   
from discord_component_creator import DiscordComponentCreator

class Controller:
    def __init__(self):
        self.crawler = Crawler()
        self.notice_creator = NoticeCreator()
        self.email = "seonu2001@kookmin.ac.kr | yyk1797@kookmin.ac.kr"
        self.latest_id = '527'

    def get_notice(self, keyword=None, article_id=None, lang='ko'):
        notice_url, title, image_urls = self.crawler.scrape_notice(keyword, article_id)
        if title is None:
            return "No notices found."
        else:
            notice = self.notice_creator.make_notice(notice_url=notice_url, title=title, image_urls=image_urls, lang=lang)
            print("controller clear")
            return notice

    async def check_new_notice(self):
        hp_latest_id = self.crawler.get_latest_id()
        if(hp_latest_id != self.latest_id):
            self.latest_id = hp_latest_id
            return self.latest_id
        else:
            return -1

    def get_email(self):
        return self.email

    def get_discord_component(self, notice, send_msg):
        try:
            view = DiscordComponentCreator.create_view(notice, send_msg)
            embed = DiscordComponentCreator.create_embed(notice)
            return view, embed  
        except Exception as e:
            print(e)
            return None, None


if __name__ == "__main__":
    # asyncio.run(main())
    controller = Controller()
    rst = controller.get_notice('추가모집', None, 'ko')
    print(rst)
    # print(rst.eventHeadDate)