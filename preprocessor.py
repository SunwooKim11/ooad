class Preprocessor:
    async def preprocess_content(self, content, translation=False):
        text = self.extract_content_from_image(content)
        processed_text = self.process_text(text)
        if translation:
            translated_text = await self.translate_text(processed_text)
            return translated_text
        return processed_text

    def extract_content_from_image(self, image_path):
        image = Image.open(image_path)
        return pytesseract.image_to_string(image)

    def process_text(self, text):
        return text

    async def translate_text(self, text):
        client = translate.Client()
        result = client.translate(text, target_language='ko')
        return result['translatedText']