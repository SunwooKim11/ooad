from googletrans import Translator, LANGUAGES

def translate(text):
    # 1. 번역기 생성
    translator = Translator()

    # 2. 언어 감지
    detected = translator.detect(text)
    src_lang = detected.lang

    # 3. 번역을 원하는 언어 입력 받기
    while True:
        dest_lang = input("원하는 원어를 입력하세요 (예: en, ko, ja 등): ").strip()
        if dest_lang in LANGUAGES:
            break  # 입력받은 언어 코드가 유효하면 반복문 종료
        else:
            print("입력하신 언어 코드가 잘못되었습니다. 다음 중 하나를 입력해주세요:", ', '.join(LANGUAGES.keys()))

    # 4. 번역 실행
    Translated = translator.translate(text, dest=dest_lang, src=src_lang)

    return Translated

