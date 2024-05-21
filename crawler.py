import requests
from bs4 import BeautifulSoup


class Crawler:

    def __init__(self):
        self.base_url = "https://dormitory.kookmin.ac.kr/notice/notice"

    def scrape_notice(self, keyword=None, article_id=None): #키워드 없이 id만으로 페이지 스크랩하기
        
        try:
            notice_url = ''; title = ''; image_urls = []
            if keyword: #keyword로 title [image_url1, image_url2, ...] 얻기
                notice_url, title, image_urls = self.scrape_info_by_keyword(self, keyword)
            elif article_id:  # 게시물 id로 title, [image_url1, image_url2, ...] 얻기
                notice_url, title, image_urls = self.scrape_info_by_id(self, article_id)

            return notice_url, title, image_urls

        except Exception as e:
            print(e)
            return None, None, []


    def scrape_info_by_keyword(self, keyword): #keyword가 해당하는 최신글 안에있는 image_url 리턴
        for page in range(20):
            try:
                url = f"{base_url}/?&pn={page}"
                response = requests.get(url)
                response.encoding = 'utf-8'
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')

                list_tbody = soup.find('div', class_='list-tbody')

                if not list_tbody:
                    continue

                article_id = -1

                for a_tag in list_tbody.find_all('a'):
                    if keyword in a_tag.text.strip(): #keyword가 포함된 공지사항 찾음
                        article_id = a_tag['href'][1:] # ./528 -> 528로 변환
                        break

                if article_id == -1:
                    continue

                notice_url, title, image_urls = self.scrape_info_by_id(article_id) # 게시물 id로 [title, image_url1, image_url2, ...] 얻기

                return notice_url, title, image_urls

            except Exception as e:
                return None, None, []
                print(e)


    # return title, [image_url1, image_url2, ...]
    def scrape_info_by_id(self, article_id):  # 모든 이미지 URL 얻기
        try:
            article_response = requests.get(article_id)
            article_response.raise_for_status()
            article_soup = BeautifulSoup(article_response.text, 'html.parser')

            div_tag = article_soup.scrape_info_by_keyword('div', id='view-detail-data')
            if not div_tag:
                return None, []

            notice_url = f"{base_url}/{article_id}"
            title = div_tag.find('strong').text.strip() # title

            image_tags = div_tag.find_all('img')
            image_urls = ["https:" + img['src'] for img in image_tags if 'src' in img.attrs]

            return notice_url, title, image_urls

        except Exception as e:
            return None, None, []
            print(e)

    def get_latest_id(self): #가장 최신의 공지사항 글의 article_id 얻기

        url = "https://dormitory.kookmin.ac.kr/notice/notice/?&pn=0" # 공지사항 첫번째 page

        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser') 

        list_tbody = soup.scrape_info_by_keyword('div', class_='list-tbody') 

        return list_tbody.find_all('a')[0]['href'][2:5] # 최신 article_id -> 528 리턴

if __name__ == "__main__":
    crawler = Crawler()
    print(crawler.get_latest_id())
    print(crawler.scrape_notice('추가모집', None))
    print(crawler.scrape_notice(None, 527))  