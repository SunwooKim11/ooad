import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
import io
import re

def preprocess_image(image):
    # 이미지 전처리: 회색조로 변환, 노이즈 제거, 대비 증가
    image = image.convert('L')
    image = image.filter(ImageFilter.MedianFilter())
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    return image

def extract_text_from_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if 'image' not in response.headers['Content-Type']:
            return "URL does not point to a valid image."
        image = Image.open(io.BytesIO(response.content))
        image = preprocess_image(image)  # 이미지 전처리 적용
        text = pytesseract.image_to_string(image, lang='kor+eng', config='--psm 6')
        return text
    
    except requests.RequestException as e:
        return f"Failed to load image: {str(e)}"
    
    except IOError as e:
        return f"Failed to process image: {str(e)}"

def find_image_and_extract_text(base_url, keyword):
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
                if keyword in a_tag.text.strip():
                    articles.append(a_tag['href'])

            if not articles:
                continue

            article_url = "https://dormitory.kookmin.ac.kr/notice/notice" + articles[0][1:]
            article_response = requests.get(article_url)
            article_response.raise_for_status()
            article_soup = BeautifulSoup(article_response.text, 'html.parser')

            div_tag = article_soup.find('div', id='view-detail-data')
            if not div_tag:
                continue

            image_tag = div_tag.find('img')
            if not image_tag or 'src' not in image_tag.attrs:
                continue
            
            image_url = "https:" + image_tag['src']
            return extract_text_from_image(image_url)
        
        except requests.RequestException as e:
            continue
        except Exception as e:
            continue

# 사용자로부터 키워드 입력받기
def crawl():
    keyword = input("Enter the keyword to search for in the posts: ")
    base_url = "https://dormitory.kookmin.ac.kr/notice/notice"
    text_from_image = find_image_and_extract_text(base_url, keyword)

    if text_from_image == None:
        text_from_image = crawl()

    return text_from_image


