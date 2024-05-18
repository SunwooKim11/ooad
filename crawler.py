class Crawler:
    async def scrape_notice(self, keyword=None, uri=None):
        try:
            if uri:
                response = requests.get(uri)
                response.raise_for_status()
                # 이미지 처리 로직
                return "Processed notice from URI"
        except requests.RequestException:
            return None