import discord

class Notice:
    def __init__(self, title, url, header):
        self.title = title
        self.url = url
        self.id = url.split('/')[-1]
        self.header = header
    
    def get_content(self):
        pass

    def get_title(self):
        return self.title

    # 디스코드 일정 이벤트 추가를 위한 날짜 형식 변환 함수
    def convert_date(self, date):
        date = date.replace('.', '-')
        idx1 = date.rfind('-')
        idx2= date.find(')')
        if idx1 != -1 or idx2 != -1:
            date = date[:idx1].strip() + 'T' + date[idx2+1:].strip()+':00'
        return date

    def get_id(self):
        return self.id

class CheckInNotice(Notice):
    def __init__(self, title, target, applyDate, acceptDate, payDate, url, header):
        super().__init__(title, url, header)
        if(applyDate.find('~') == -1):
            self.applyHeadDate = ""
            self.applyTailDate = ""
        else:
            head = applyDate.split('~')[0].strip()
            tail = applyDate.split('~')[1].strip()
            self.applyHeadDate = self.convert_date(head)
            self.applyTailDate = self.convert_date(tail)

        self.target = target
        self.applyDate = applyDate
        self.acceptDate = acceptDate
        self.payDate = payDate
    
    def get_content(self):
        content = f'{self.header[0]}: {self.target}\n{self.header[1]}:{self.applyDate}\n{self.header[2]}: {self.acceptDate}\n{self.header[3]}: {self.payDate}\n'
        return content

class CheckOutNotice(Notice):
    def __init__(self, title, target, outDate, moveDate, url, header):
        super().__init__(title, url, header)
        self.outHeadDate = self.convert_date(outDate.split('~')[0].strip())
        self.outTailDate = self.convert_date(outDate.split('~')[1].strip())
        self.target = target
        self.outDate = outDate
        self.moveDate = moveDate

    def get_content(self):
        content = f'{self.header[0]}: {self.target}\n{self.header[1]}: {self.outDate}\n{self.header[2]}: {self.moveDate}\n'
        return content