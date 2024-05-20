import requests
import json
import base64
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup


class Crawler:

    base_url = "https://dormitory.kookmin.ac.kr/notice/notice"
    

    async def scrape_notice(self, keyword=None, id=None): #키워드 없이 id만으로 페이지 스크랩하기
        try:
            if keyword: #keyword만으로 img_url 얻기

                image_url = self.find_image_and_extract_text(self.base_url,keyword)

                return image_url #keyword를 포함하는 가장 최신 공지사항 글 안에있는 image_url 리턴
            

            elif id:  #키워드 없이 id만으로 페이지 스크랩하기

                # response = requests.get(id)
                # response.raise_for_status()

                url = self.base_url + '/id' #id에 해당하는 url

                return self.get_image_urls(url) # id에 해당하는 url의 img_url 리턴
            
        except requests.RequestException:
            return None
    

    def find_image_and_extract_text(self,base_url, keyword): #keyword가 해당하는 최신글 안에있는 image_url 리턴
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

                articles = []

                for a_tag in list_tbody.find_all('a'):
                    if keyword in a_tag.text.strip(): #keyword가 포함된 공지사항 찾음
                        articles.append(a_tag['href'])
                        break

                if not articles:
                    continue

                article_url = "https://dormitory.kookmin.ac.kr/notice/notice" + articles[0][1:] # keyword가 포함된 공지사항글의 주소

                imgae_url = self.get_image_urls(article_url) #글 안에잇는 image_url 리턴

                return imgae_url

            
            except requests.RequestException as e:
                continue
            except Exception as e:
                continue


    def get_image_urls(self,article_url):  # 모든 이미지 URL 얻기
        try:
            article_response = requests.get(article_url)
            article_response.raise_for_status()
            article_soup = BeautifulSoup(article_response.text, 'html.parser')

            div_tag = article_soup.find('div', id='view-detail-data')
            if not div_tag:
                return [], None

            image_tags = div_tag.find_all('img')
            image_urls = ["https:" + img['src'] for img in image_tags if 'src' in img.attrs]
            
            return image_urls
        
        except requests.RequestException as e:
            return []
    
    def get_latest_id(): #가장 최신의 공지사항 글의 id 얻기

        url = "https://dormitory.kookmin.ac.kr/notice/notice/?&pn=0" # 공지사항 첫번째 page

        response = requests.get(url)
        response.encoding = 'utf-8'
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser') 

        list_tbody = soup.find('div', class_='list-tbody') 
        
        return list_tbody.find_all('a')[0]['href'][2:5] # 최신 id -> 528 리턴

