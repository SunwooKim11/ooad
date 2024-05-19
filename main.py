import crawling 
import translate


while(True):

    action = input("\n1 : keyword가 들어간 공지사항 받기 \n2 : 번역된 언어로 공지사항 받기\n")

    text = ""
    if action == "1":
        try:
            text = crawling.crawl()
            print()
            print(text)
        except:
            continue

    elif action == "2":
        text = crawling.crawl()
        translate_text = translate.translate(text)
        print()
        print(translate_text.text)