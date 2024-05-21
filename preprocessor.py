import requests
import json
import base64
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from notice import *

# 네이버 클로바 OCR API 설정
API_URL = 'https://jn05k0ttzf.apigw.ntruss.com/custom/v1/31034/a6e67fd060274f7919b7dbfe4e0f5181d60e74f72398e4126bc6339a04e73d08/general'
API_SECRET = 'WVd5T0xxR25Sa1VvVGFLUFZLallBUnJudHFmZXFHdVg='

class Preprocessor:

    def make_notice(self, notice_url, title, image_urls, lang='ko'):  #image_urls => content list 

        #이미지에서 텍스트 뽑아내기 / content : list라 for 문 돌려서 텍스트를 받아야함
        contents = [self.extract_text_from_image_url(image_url) for image_url in image_urls] # contents -> list 형태
        # print(contents[0])

        processed_text = self.extract_infos(notice_url, title, contents) #전처리된 텍스트

        return processed_text

    def extract_text_from_image_url(self, image_url): #image_url에서 텍스트 뽑아내기
        headers = {
            'X-OCR-SECRET': API_SECRET,
            'Content-Type': 'application/json'
        }

        try:
            #img_url에서 이미지를 열어 api에 전달하기
            response = requests.get(image_url) 
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
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
            
            content = api_response.json() #이미지에서 뽑아낸 텍스트
            contents = self.parse_ocr_result(content)  #contents 줄바꿈 처리하기

            return contents
        
        except requests.RequestException as e:
            return f"Failed to call API: {str(e)}"


    #contents 예쁘게 뽑기
    def parse_ocr_result(self, content):
        if 'images' not in content:
            return ""
        
        fields = content['images'][0]['fields']
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


    #전처리하기 -> 대상, 일시 등등 뽑아내기
    def extract_infos(self, notice_url, title, contents): 
        
        if title is None:
            return []

        print(title)
        article_type, headers = self.set_headers(title) #제목에 있는 단어에 따라 keyword를 바꿈
        # print(headers)
        filtered_lines = []
        found_keywords = set()
        print(contents)
        flag = True
        for content in contents:  # 제목 이후의 라인들만 처리
            lines = content.split('\n')
            for line in lines:
                for header in headers:
                    if header in line and header not in found_keywords: 
                        print(line.find(header))
                        st_idx = line.find(header)+6 # hard coding
                        filtered_lines.append(line[st_idx:])
                        found_keywords.add(header)
                        if(len(filtered_lines) == len(headers)):
                            flag = False
                        break  # Once a header is found, stop checking other headers for this line
                if not flag:
                    break
            if not flag:
                break
        print(found_keywords)
        
        notice = None
        
        if(article_type == 1): # 2학기 정기모집
            notice = CheckInNotice(title, filtered_lines[0], filtered_lines[1], None, None, notice_url, headers)
        elif(article_type == 2): # 나머지 추가모집, 정기모집
            notice = CheckInNotice(title, filtered_lines[0], filtered_lines[1], filtered_lines[2], filtered_lines[3], notice_url, headers)
        elif(article_type == 3):
            notice =CheckOutNotice(title, filtered_lines[0], filtered_lines[1], notice_url, headers)
        
        return notice
    
        # 정기모집을 입력했을 때
        # ['2024학년도 재학 및 복학예정자(외국인학생, 대학원생, 수료생 제외)', <신청대상>
        #  '2023.12.19.(화) ~ 2024.01.09.(화)', <신청기간>
        #  '2024.01.15.(월) 15시 ~', <합격발표>
        #  '2024.01.15.(월) ~ 2024.01.21.(일)'] <관비납부>
        #  리스트로 리턴됨

    def set_headers(self, title):
        article_type = 0; headers = []
        if '정기모집' in title and '2학기' in title:
            article_type = 1
            headers = ['납부대상', '납부기간']
        elif any(term in title for term in ['정기모집', '추가모집']):
            article_type = 2
            headers = ['신청대상', '신청기간', '합격발표', '관비납부']
        elif '퇴실' in title and not any(term in title for term in ['택배', '입실', '차량', '환불']):
            article_type = 3
            headers = ['대 상', '일 시']
        
        return article_type, headers



    async def translate_text(self, contents):
        client = translate.Client()
        content = client.translate(contents, target_language='ko')
        return content['translatedText']

if __name__ == "__main__":
    test_img_url = ['https://wfile.kookmin.ac.kr/files-v2/2024학년도 생활관생 추가모집 및 충원대기자 모집 안내 - 재학생 및 신입생001.png?type=image&id=584a4f6742e919ed0d5deacb1cd889d4',
                    'https://wfile.kookmin.ac.kr/files-v2/2024%ED%95%99%EB%85%84%EB%8F%84%20%EC%83%9D%ED%99%9C%EA%B4%80%EC%83%9D%20%EC%B6%94%EA%B0%80%EB%AA%A8%EC%A7%91%20%EB%B0%8F%20%EC%B6%A9%EC%9B%90%EB%8C%80%EA%B8%B0%EC%9E%90%20%EB%AA%A8%EC%A7%91%20%EC%95%88%EB%82%B4%20-%20%EC%9E%AC%ED%95%99%EC%83%9D%20%EB%B0%8F%20%EC%8B%A0%EC%9E%85%EC%83%9D002.png?type=image&id=f04605e35fcad99f7efc256f03e99c8b']
    test_title = '2024학년도 생활관생 추가모집 및 충원대기자 모집 안내 - 재학생 및 신입생'
    preprocessor = Preprocessor()
    # rst = preprocessor.extract_text_from_image_url(test_img_url)
    rst = preprocessor.make_notice(test_title,test_img_url)
    print(rst)