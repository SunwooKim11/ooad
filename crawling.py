import requests
import json
import base64
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

# 네이버 클로바 OCR API 설정
API_URL = 'https://jn05k0ttzf.apigw.ntruss.com/custom/v1/31034/a6e67fd060274f7919b7dbfe4e0f5181d60e74f72398e4126bc6339a04e73d08/general'
API_SECRET = 'WVd5T0xxR25Sa1VvVGFLUFZLallBUnJudHFmZXFHdVg='

def extract_text_from_image_url(image_url):
    headers = {
        'X-OCR-SECRET': API_SECRET,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(image_url)
        response.raise_for_status()

        # 이미지를 메모리에서 처리
        image = Image.open(BytesIO(response.content))
        image.show()
        
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        data = {
            'version': 'V1',
            'requestId': 'sample_id',
            'timestamp': 0,
            'images': [
                {
                    'name': 'sample_image',
                    'format': 'jpg',
                    'data': image_base64
                }
            ]
        }

        api_response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        api_response.raise_for_status()
        
        result = api_response.json()
        text = parse_ocr_result(result)
        return text
    
    except requests.RequestException as e:
        return f"Failed to call API: {str(e)}"

# 이미지에서 텍스트 추출
def parse_ocr_result(result): 
    if 'images' not in result:
        return ""
    
    fields = result['images'][0]['fields']
    lines = []
    current_line = []
    current_y = None
    line_gap_threshold = 10  # Adjust this threshold as needed
    
    for field in fields:
        infer_text = field['inferText']
        vertices = field['boundingPoly']['vertices']
        y_coordinate_top = vertices[0]['y']
        
        if current_y is None:
            current_y = y_coordinate_top
        
        if abs(y_coordinate_top - current_y) > line_gap_threshold:
            lines.append(' '.join(current_line))
            current_line = []
            current_y = y_coordinate_top
        
        current_line.append(infer_text)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)



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

            image_url, article_id = get_image_url_and_id(article_url)
            return extract_text_from_image_url(image_url), article_url, article_id
        
        except requests.RequestException as e:
            continue
        except Exception as e:
            continue

def get_image_url_and_id(article_url): # url id 얻기
    try:
        article_response = requests.get(article_url)
        article_response.raise_for_status()
        article_soup = BeautifulSoup(article_response.text, 'html.parser')

        div_tag = article_soup.find('div', id='view-detail-data')
        if not div_tag:
            return None, None

        image_tag = div_tag.find('img')
        if not image_tag or 'src' not in image_tag.attrs:
            return None, None
        
        image_url = "https:" + image_tag['src']
        article_id = article_url.split('/')[-1][:3]
        return image_url, article_id
    
    except requests.RequestException as e:
        return None, None

# 사용자로부터 키워드 입력받기
def crawl():
    keyword = input("Enter the keyword to search for in the posts: ")
    base_url = "https://dormitory.kookmin.ac.kr/notice/notice"

    result,result_url, article_id = find_image_and_extract_text(base_url, keyword) # 추출 텍스트, 페이지 url, url_id 

    if result is None:
        result = crawl()

    print("result_url :" , result_url)
    print(f"Article ID: {article_id}")

    return result
