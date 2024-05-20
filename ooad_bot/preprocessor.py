import requests
import json
import base64
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

# 네이버 클로바 OCR API 설정
API_URL = 'https://jn05k0ttzf.apigw.ntruss.com/custom/v1/31034/a6e67fd060274f7919b7dbfe4e0f5181d60e74f72398e4126bc6339a04e73d08/general'
API_SECRET = 'WVd5T0xxR25Sa1VvVGFLUFZLallBUnJudHFmZXFHdVg='

class Preprocessor:

    async def preprocess_content(self, content, translation=False, lang='ko'):  #content -> img_url

        text = self.extract_content_from_image(content) #이미지에서 텍스트 뽑아내기

        processed_text = self.process_text(text) #전처리된 텍스트
        if translation:
            translated_text = await self.translate_text(processed_text) #번역함
            return translated_text
        return processed_text


    def extract_content_from_image(self, image_url): #image_url에서 텍스트 뽑아내기
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
            
            result = api_response.json() #이미지에서 뽑아낸 텍스트
            text = self.parse_ocr_result(result)  #text 줄바꿈 처리하기

            return text
        
        except requests.RequestException as e:
            return f"Failed to call API: {str(e)}"


    #text 예쁘게 뽑기
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


    #전처리하기 -> 대상, 일시 등등 뽑아내기
    def process_text(self, texts): 
        
        if not texts:
            return []

        title = texts[0][:30] 

        keywords = self.determine_keywords(title) #제목에 있는 단어에 따라 keyword를 바꿈
        filtered_lines = []
        found_keywords = set()

        for result in texts:  # 제목 이후의 라인들만 처리
            lines = result.split('\n')
            for line in lines:
                for keyword in keywords:
                    if keyword in line[:10] and keyword not in found_keywords: 
                        filtered_lines.append(line)
                        found_keywords.add(keyword)
                        break  # Once a keyword is found, stop checking other keywords for this line
        
        return texts
    
        # 정기모집을 입력했을 때
        # ['2024학년도 재학 및 복학예정자(외국인학생, 대학원생, 수료생 제외)', <신청대상>
        #  '2023.12.19.(화) ~ 2024.01.09.(화)', <신청기간>
        #  '2024.01.15.(월) 15시 ~', <합격발표>
        #  '2024.01.15.(월) ~ 2024.01.21.(일)'] <관비납부>
        #  리스트로 리턴됨

    def determine_keywords(title):

        if '2학기' in title:
            return ['납부대상', '납부기간']
        elif any(term in title for term in ['정기모집', '추가모집']) and '2학기' not in title:
            return ['신청대상', '신청기간', '합격발표', '관비납부']
        elif '퇴실' in title and not any(term in title for term in ['택배', '입실', '차량', '환불']):
            return ['대상', '일시']
        else:
            return []



    async def translate_text(self, text):
        client = translate.Client()
        result = client.translate(text, target_language='ko')
        return result['translatedText']