# Project Nmae
- 🔗 Discord 국민대 기숙사 공지 봇

# 🌐 About the Project
- Discord 국민대 기숙사 공지 봇은  기숙사 홈페이지의 공지사항을 주기적으로 스크래핑하여, Discord 봇으로 제공합니다.

## 📚 Projcet Vision

- 기숙사 입주 등 놓치기 쉬운 학교 알림을 디스코드 봇을 통해 알려주는 서비스를 만든다.
- 서버가 주기적으로 공지사항 사이트를 스크래핑하고, 공지가 올라오면 디스코드 봇으로 알림을 보내준다.
- 사용자가 원한다면, 마감 공고 전 리마인드 알림을 보내, 공고를 놓치지 않게 해준다

## Project Scope
1. 기숙사 공지사항 글 자동 제공
   - 주기적으로 공지사항 리스트를 스크래핑하여, 새로 올라온 공지 봇으로 제공
   - ![image](https://github.com/user-attachments/assets/e6ec822d-f1b1-4aed-9cf5-56d9b9581a23)
2. 관심 키워드가 포함된 최신 글 제공
   - 사용자가 명령어로 키워드 입력 시, 그와 관련한 가장 최근 공지를 봇으로 보내줌.
   - ex. /keyword '입실' 시, 2025-1학기 생활관 입실 및 호실배정 안내
   - ![image](https://github.com/user-attachments/assets/479ce6f7-6f3f-4f2c-8009-dbb321039cba)

3. 외국인 학생을 위한 번역 기능 제공
   - ex. Google Translate API로 5개국어(한국어, 영어, 중국어, 일본어, 러시아어) 제공
   - ![image](https://github.com/user-attachments/assets/41fa5af4-4ea6-4767-a28b-a1ee26abbf28)
   - ![image](https://github.com/user-attachments/assets/90b9995e-7797-4237-9e6d-f26a73654f45)


4. Discord 서버에 이벤트 추가하기
   - 이벤트(캘린더) 개념. 공지 일정을 Discord 캘린더에 등록한다.
   - ![image](https://github.com/user-attachments/assets/9b99b905-8aef-4df0-9ec8-bb2105713de5)
   - ![image](https://github.com/user-attachments/assets/b4444f74-97dd-4ee0-a327-6d0de58b0395)


5. 문의하기 기능 제공
   - 개발자 이메일 주소 제공 -> 추후 채팅 기능으로 변경
   - ![image](https://github.com/user-attachments/assets/8f23b3d4-4b83-4b64-9a13-337161b89663)

# 🚀 Installation
- todo
# 🔧 Built With

- Python - Core language
- Discord.py - Discord Bot Framework
- BeautifulSoup - Web Scraping
- Google Translation API - Translation Service
- OCR API - Text Recognition from Images

