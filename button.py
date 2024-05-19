from event import create_event
import discord

lang_label = {
    'ko': '한국어',
    'en': '영어',
    'zh-CN': '중국어',
    'ja': '일본어',
    'ru': '러시아어'
}

class MyButton(discord.ui.Button):
    def __init__(self, kind, notice, url_id, send_msg):
        self.send_msg = send_msg
        try:
            if notice is None:
                custom_id = kind + '_' + url_id
                label = lang_label[kind]
                self.notice = None
                style = discord.ButtonStyle.primary
            else:  # notice가 있을 때
                self.notice = notice
                if kind == 'add_sch_button':
                    custom_id = "1_" + getattr(notice, 'id')
                    label = "일정추가"
                    style = discord.ButtonStyle.primary
                elif kind == 'trans_button':
                    custom_id = "2_" + getattr(notice, 'id')
                    label = "번역"
                    style = discord.ButtonStyle.secondary
        except Exception as e:
            print(e)
        finally:
            super().__init__(label=label, style=style, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction):
        try:
            id = interaction.data['custom_id']
            if id.startswith('1'):
                print('add_sch_button')
                print(self.notice.applyHeadDate, self.notice.applyTailDate)
                await create_event(self.notice)
                await interaction.response.send_message("add_sch_button")
            elif id.startswith('2'):
                print('trans_button')
                await interaction.response.send_message("언어를 선택해주세요", view=self.get_lang_buttons(self.notice.get_id()))
            else:
                lang = id.split('_')[0]
                url_id = id.split('_')[1]
                await self.send_msg(ctx_or_interaction=interaction, lang=lang, keyword=None, url_id=url_id)
        except Exception as e:
            print(e)
        finally:
            pass

    def get_lang_buttons(self, url_id):
        view = discord.ui.View()
        for lang in lang_label.keys():
            view.add_item(MyButton(kind=lang, notice=None, url_id=url_id, send_msg=self.send_msg))
        return view