
"""
1학기 정기모집 신청기간: 2022.12.20.(화) ~ 2022.12.30.(금)
1학기 추가모집 신청기간 : 2023.10.06.(목) 11시 ~ 10.12.(수) 13시
1학기 퇴실기간 : 2023.06.19 (월) ~ 06.23 (금) 10시 ~ 17시
여름학기 추가모집 신청기간 : 2023.06.05 (월) 11:00 ~ 2023.06.11 (일) 13:00
여름학기 퇴실기간 : 2023.08.21 (월) ~ 08.25 (금) 10시 ~ 17시
2학기 정기모집 납부기간 : 2024.06.03.(수) 11:00 ~ 2024.06.09.(화) 13:00
2학기 추가모집 신청기간 : 2023.10.06.(목) 11:00 ~ 10.12.(수) 13:00
2학기 퇴실기간 : 2023.12.19 (화) ~ 12.23 (토) 10시 ~ 17시
겨울학기 추가모집 신청기간 : 2023.12.05 (화) 15:00 ~ 2023.12.11 (월) 13:00 
겨울학기 퇴실기간: 2024.02.19 (월) ~ 02.23 (금) 10시 ~ 17시

1. 1학기 정기모집 신청기간:
    yyyy.mm.dd.(요일) ~ yyyy.mm.dd.(요일)
2. 1학기 추가모집 신청기간:
    yyyy.mm.dd.(요일) hh시 ~ yyyy.mm.dd.(요일) hh시
3. 1학기 퇴실기간, 여름학기 퇴실기간, 2학기 퇴실기간, 겨울학기 퇴실기간:
    yyyy.mm.dd (요일) ~ yyyy.mm.dd (요일) hh시 ~ hh시
4. 2학기 추가모집 신청기간:
    yyyy.mm.dd.(요일) hh:mm ~ mm.dd.(요일) hh:mm
5. 2학기 정기모집 납부기간, 여름학기 추가모집 신청기간, 겨울학기 추가모집 신청기간:
    yyyy.mm.dd.(요일) hh:mm ~ yyyy.mm.dd.(요일) hh:mm
"""
import re
from datetime import datetime

def convert_date(date_str):
    try:
        # 패턴 1: yyyy.mm.dd.(요일) ~ yyyy.mm.dd.(요일)
        match = re.match(r'(\d{4}\.\d{2}\.\d{2}\.\(\w\)) ~ (\d{4}\.\d{2}\.\d{2}\.\(\w\))', date_str)
        if match:
            head = match.group(1)
            tail = match.group(2)
            head_date = datetime.strptime(head[:10], '%Y.%m.%d').strftime('%Y-%m-%dT00:00:00')
            tail_date = datetime.strptime(tail[:10], '%Y.%m.%d').strftime('%Y-%m-%dT00:00:00')
            return head_date, tail_date

        # 패턴 2: yyyy.mm.dd.(요일) hh시 ~ yyyy.mm.dd.(요일) hh시
        match = re.match(r'(\d{4}\.\d{2}\.\d{2}\.\(\w\) \d{2}시) ~ (\d{4}\.\d{2}\.\d{2}\.\(\w\) \d{2}시)', date_str)
        if match:
            head = match.group(1)
            tail = match.group(2)
            head_date = datetime.strptime(head[:15], '%Y.%m.%d. %H시').strftime('%Y-%m-%dT%H:00:00')
            tail_date = datetime.strptime(tail[:15], '%Y.%m.%d. %H시').strftime('%Y-%m-%dT%H:00:00')
            return head_date, tail_date

        # 패턴 3: yyyy.mm.dd.(요일) ~ yyyy.mm.dd.(요일) hh시 ~ hh시
        match = re.match(r'(\d{4}\.\d{2}\.\d{2}\.\(\w\)) ~ (\d{4}\.\d{2}\.\d{2}\.\(\w\)) (\d{2}시 ~ \d{2}시)', date_str)
        if match:
            head = match.group(1)
            tail = match.group(2)
            times = match.group(3).split(' ~ ')
            head_time = times[0].replace('시', ':00:00')
            tail_time = times[1].replace('시', ':00:00')
            head_date = datetime.strptime(head[:10], '%Y.%m.%d').strftime('%Y-%m-%dT') + head_time
            tail_date = datetime.strptime(tail[:10], '%Y.%m.%d').strftime('%Y-%m-%dT') + tail_time
            return head_date, tail_date

        # 패턴 4: yyyy.mm.dd.(요일) hh:mm ~ mm.dd.(요일) hh:mm
        match = re.match(r'(\d{4}\.\d{2}\.\d{2}\.\(\w\) \d{2}:\d{2}) ~ (\d{2}\.\d{2}\.\(\w\) \d{2}:\d{2})', date_str)
        if match:
            head = match.group(1)
            tail = match.group(2)
            head_date = datetime.strptime(head[:17], '%Y.%m.%d. %H:%M').strftime('%Y-%m-%dT%H:%M:00')
            current_year = datetime.now().year
            tail_date = datetime.strptime(f"{current_year}.{tail[:11]}", '%Y.%m.%d.').strftime('%Y-%m-%dT') + tail[12:].replace(':', ':00:00')
            return head_date, tail_date

        # 패턴 5: yyyy.mm.dd.(요일) hh:mm ~ yyyy.mm.dd.(요일) hh:mm
        match = re.match(r'(\d{4}\.\d{2}\.\d{2}\.\(\w\) \d{2}:\d{2}) ~ (\d{4}\.\d{2}\.\d{2}\.\(\w\) \d{2}:\d{2})', date_str)
        if match:
            head = match.group(1)
            tail = match.group(2)
            head_date = datetime.strptime(head[:17], '%Y.%m.%d. %H:%M').strftime('%Y-%m-%dT%H:%M:00')
            tail_date = datetime.strptime(tail[:17], '%Y.%m.%d. %H:%M').strftime('%Y-%m-%dT%H:%M:00')
            return head_date, tail_date

        raise ValueError("Date format not recognized")
    except Exception as e:
        print(f"Error in convert_date: {e}")
        return None, None

# Example Notice classes for testing
class Notice:
    def __init__(self, title, url, header):
        self.title = title
        self.url = url
        self.id = url.split('/')[-1]
        self.header = header
        self.eventHeadDate = ""
        self.eventTailDate = ""

    def get_content(self):
        pass

    def get_title(self):
        return self.title

    def get_id(self):
        return self.id

class CheckInNotice(Notice):
    def __init__(self, title, target, applyDate, acceptDate, payDate, url, header):
        super().__init__(title, url, header)
        try:
            self.target = target
            self.applyDate = applyDate
            self.acceptDate = acceptDate
            self.payDate = payDate

            if applyDate is None:  # 2학기 정기모집은 payDate만 있음
                self.eventHeadDate, self.eventTailDate = convert_date(payDate)
            else:
                self.eventHeadDate, self.eventTailDate = convert_date(applyDate)

            if self.eventHeadDate is None or self.eventTailDate is None:
                raise ValueError("Date format not recognized")
        except Exception as e:
            print(e)
        finally:
            pass

    def get_content(self):
        content = f'{self.header[0]}: {self.target}\n{self.header[1]}: {self.applyDate}\n{self.header[2]}: {self.acceptDate}\n{self.header[3]}: {self.payDate}\n'
        return content

class CheckOutNotice(Notice):
    def __init__(self, title, target, outDate, url, header):
        super().__init__(title, url, header)
        self.target = target
        self.outDate = outDate

        try:
            self.eventHeadDate, self.eventTailDate = convert_date(outDate)
            if self.eventHeadDate is None or self.eventTailDate is None:
                raise ValueError("Date format not recognized")
        except Exception as e:
            print(e)
            self.eventHeadDate, self.eventTailDate = None, None

    def get_content(self):
        content = f'{self.header[0]}: {self.target}\n{self.header[1]}: {self.outDate}\n'
        return content
