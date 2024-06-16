import discord
from notice_model import *
from button import MyButton

class DiscordComponentCreator:    
    def __init__(self):
        self.notice = None
    
    @staticmethod
    def create_view(notice, send_msg):
        view = discord.ui.View()
        view.add_item(MyButton(kind='add_sch_button', notice=notice, url_id=notice.get_id(), send_msg=send_msg))
        view.add_item(MyButton(kind='trans_button', notice=notice, url_id=notice.get_id(), send_msg=send_msg))

        return view
    
    @staticmethod
    def create_embed(notice):
        embed = discord.Embed(title=notice.title, url=notice.url, color=0x00ff00)
        header = notice.header
        if isinstance(notice, CheckInNotice):
            attr = ['target', 'applyDate', 'acceptDate', 'payDate']
        elif isinstance(notice, CheckOutNotice):
            attr = ['target', 'outDate', 'moveDate']
        else:
            pass
        header_len = 0 if header is None else len(header)
        for i in range(header_len):
            embed.add_field(name=header[i], value=getattr(notice, attr[i]), inline=False)

        return embed
        
    @staticmethod
    def set_notice(notice):
        self.notice = notice