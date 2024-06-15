from googletrans import Translator, LANGUAGES

def translate(text, dest_lang='en'):
    # 1. 번역기 생성
    translator = Translator()

    # 2. 언어 감지
    detected = translator.detect(text)
    src_lang = detected.lang
    print(f"Detected language: {src_lang}")

    # 3. 번역 실행
    translated = translator.translate(text, src=src_lang, dest=dest_lang)

    return translated.text

if __name__ == "__main__":
    original_text = "2024-1학기 생활관 퇴실 및 호실이동 안내"
    translated_text = translate(original_text)
    print("원문:", original_text)
    print("번역:", translated_text)
