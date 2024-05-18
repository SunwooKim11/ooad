import discord

class Notice:
    def __init__(self, title, target, url):
        self.title = title
        self.target = target
        self.url = url
        self.id = url.split('/')[-1]
    
    def get_content(self):
        content = f'모집대상: {self.target}\n'
        return content

    def get_title(self):
        return self.title

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
    def __init__(self, title, target, applyDate, acceptDate, payDate, url):
        super().__init__(title, target, url)
        head = applyDate.split('~')[0].strip()
        tail = applyDate.split('~')[1].strip()
        self.applyDate = applyDate
        self.applyHeadDate = self.convert_date(head)
        self.applyTailDate = self.convert_date(tail)
        self.acceptDate = acceptDate
        self.payDate = payDate
    
    def get_content(self):
        content = f'모집대상: {self.target}\n모집기간: {self.applyDate}\n합격자 발표일: {self.acceptDate}\n입금기간: {self.payDate}\n'
        return content

class CheckOutNotice(Notice):
    def __init__(self, title, target, outDate, moveDate, url):
        super().__init__(title, target, url)
        self.outHeadDate = self.convert_date(outDate.split('~')[0].strip())
        self.outTailDate = self.convert_date(outDate.split('~')[1].strip())
        self.moveDate = moveDate

    def get_content(self):
        content = f'모집대상: {self.target}\n퇴실기간: {self.outHeadDate} ~ {self.outTailDate}\n호실이동 기간: {self.moveDate}\n'
        return content
