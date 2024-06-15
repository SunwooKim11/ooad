from event import create_event
import discord
from notice import CheckInNotice

lang_label = {
    'ko': '한국어',
    'en': '영어',
    'zh-CN': '중국어',
    'ja': '일본어',
    'ru': '러시아어'
}
lang_style = {
    'ko': discord.ButtonStyle.primary,
    'en': discord.ButtonStyle.secondary,
    'zh-CN': discord.ButtonStyle.success,
    'ja': discord.ButtonStyle.danger,
    'ru': discord.ButtonStyle.primary
}

class MyButton(discord.ui.Button):
    def __init__(self, kind, notice, url_id, send_msg):
        self.send_msg = send_msg
        self.kind = kind
        self.notice = notice
        self.url_id = url_id

        if notice is None:
            custom_id = kind + '_' + url_id
            label = lang_label[kind]
            style = lang_style[kind]
        else:
            if kind == 'add_sch_button':
                custom_id = "1_" + getattr(notice, 'id')
                label = "일정추가"
                style = discord.ButtonStyle.primary
            elif kind == 'trans_button':
                custom_id = "2_" + getattr(notice, 'id')
                label = "번역"
                style = discord.ButtonStyle.secondary

        super().__init__(label=label, style=style, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()  # 상호작용 지연

            id = interaction.data['custom_id']
            if id.startswith('1'):
                print('add_sch_button')
                if isinstance(self.notice, CheckInNotice):
                    print(self.notice.applyDate)
                else:
                    print(self.notice.outDate)
                await create_event(self.notice)
                await interaction.followup.send("스케줄 추가 완료!")
            elif id.startswith('2'):
                print('trans_button')
                view = self.get_lang_buttons(self.notice.get_id())
                await interaction.followup.send("언어를 선택해주세요", view=view)
            else:
                lang = id.split('_')[0]
                url_id = id.split('_')[1]
                await self.send_msg_later(interaction, lang, url_id)
        except Exception as e:
            print(e)
        finally:
            pass

    async def send_msg_later(self, interaction, lang, url_id):
        await interaction.followup.send("번역을 처리 중입니다. 잠시만 기다려주세요...")
        # 번역 작업을 비동기로 수행하여 상호작용 시간을 초과하지 않도록 합니다.
        await self.send_msg(ctx_or_interaction=interaction.channel, lang=lang, keyword=None, url_id=url_id)

    def get_lang_buttons(self, url_id):
        view = discord.ui.View()
        for lang in lang_label.keys():
            view.add_item(MyButton(kind=lang, notice=None, url_id=url_id, send_msg=self.send_msg))
        return view