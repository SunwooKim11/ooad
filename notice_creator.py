import requests
import json
import base64
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from notice_model import *
from translator import translate

# 네이버 클로바 OCR API 설정
API_URL = 'https://jn05k0ttzf.apigw.ntruss.com/custom/v1/31034/a6e67fd060274f7919b7dbfe4e0f5181d60e74f72398e4126bc6339a04e73d08/general'
API_SECRET = 'WVd5T0xxR25Sa1VvVGFLUFZLallBUnJudHFmZXFHdVg='

class NoticeCreator:

    def make_notice(self, notice_url, title, image_urls, lang='ko'):  # image_urls => content list 

        # 이미지에서 텍스트 뽑아내기 / content : list라 for 문 돌려서 텍스트를 받아야함
        contents = [self.extract_text_from_image_url(image_url) for image_url in image_urls]  # contents -> list 형태

        notice = self.extract_infos(notice_url, title, contents, lang)  # 전처리된 텍스트

        return notice

    def extract_text_from_image_url(self, image_url):  # image_url에서 텍스트 뽑아내기
        headers = {
            'X-OCR-SECRET': API_SECRET,
            'Content-Type': 'application/json'
        }

        try:
            # img_url에서 이미지를 열어 api에 전달하기
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

            content = api_response.json()  # 이미지에서 뽑아낸 텍스트
            contents = self.parse_ocr_result(content)  # contents 줄바꿈 처리하기

            return contents

        except requests.RequestException as e:
            return f"Failed to call API: {str(e)}"

    # contents 예쁘게 뽑기
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

    # 전처리하기 -> 대상, 일시 등등 뽑아내기
    def extract_infos(self, notice_url, title, contents, lang):
        try:
            article_type, headers = self.set_headers(title)  # 제목에 있는 단어에 따라 keyword를 바꿈
            len_header = 4 if(article_type == 2) else 2
            title = translate(title, lang) # title 원하는 언어로 설정
            if article_type != 0:
                filtered_lines = []
                found_keywords = []
                flag = True
                for content in contents:  # 제목 이후의 라인들만 처리
                    lines = content.split('\n')
                    for line in lines:
                        for header in headers:
                            if header in line and header not in found_keywords:
                                print(line)
                                st_idx = line.find(":") + 2  # hard coding
                                filtered_lines.append(line[st_idx:])
                                found_keywords.append(header)
                                if len(filtered_lines) == len_header:
                                    flag = False
                                break  # Once a header is found, stop checking other headers for this line
                        if not flag:
                            break
                    if not flag:
                        break
                filtered_lines[0] = translate(filtered_lines[0], lang) # target(대상) 원하는 언어로 설정
                print(found_keywords)
                print(filtered_lines)
                print(article_type)
                notice = None
                if article_type == 1:  # 2학기 정기모집
                    notice = CheckInNotice(title, filtered_lines[0], filtered_lines[1], None, None, notice_url, found_keywords)
                elif article_type == 2:  # 나머지 추가모집, 정기모집
                    notice = CheckInNotice(title, filtered_lines[0], filtered_lines[1], filtered_lines[2], filtered_lines[3], notice_url, found_keywords)
                elif article_type == 3:
                    notice = CheckOutNotice(title, filtered_lines[0], filtered_lines[1], notice_url, found_keywords)
            else:
                notice = Notice(title=title, url=notice_url, header=[])
            return notice
        except Exception as e:
            print(found_keywords)
            print(filtered_lines)
            print(e)
            return None

    def set_headers(self, title):
        article_type = 0
        headers = []
        if '정기모집' in title and '2학기' in title:
            article_type = 1
            headers = ['납부대상', '납부기간']
        elif any(term in title for term in ['정기모집', '추가모집']):
            article_type = 2
            headers = ['신청대상', '신청기간', '합격발표', '관비납부', '납부기간']
        elif '퇴실' in title and not any(term in title for term in ['택배', '입실', '차량', '환불']):
            article_type = 3
            headers = ['대상', '일시']

        return article_type, headers

if __name__ == "__main__":
    test_url = 'https://dormitory.kookmin.ac.kr/notice/notice/528'
    test_title = '2024-1학기 생활관 퇴실 및 호실이동 안내'
    test_img_url = ['https://wfile.kookmin.ac.kr/files-v2/2024-1%ED%95%99%EA%B8%B0%20%ED%87%B4%EC%8B%A4%20%EB%B0%8F%20%ED%98%B8%EC%8B%A4%EC%9D%B4%EB%8F%99%20%EC%95%88%EB%82%B4001001.png?type=image&id=a919418bcf0f83aa3332ad36256d0408']
    preprocessor = NoticeCreator()
    notice = preprocessor.make_notice(test_url, test_title, test_img_url, 'en')
    print(notice.title, notice.target, notice.outDate, notice.url, notice.header)