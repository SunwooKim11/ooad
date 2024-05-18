from event import create_event
import discord

# button api 참고
# https://discordpy.readthedocs.io/en/latest/interactions/api.html#id1

class MyButton(discord.ui.Button):
    def __init__(self, kind, notice):
        try:
            if kind == 'add_sch_button':
                custom_id = "1-" + getattr(notice, 'id')
                label = "일정추가"
                style = discord.ButtonStyle.primary
            elif kind == 'trans_button':
                custom_id = "2-" + getattr(notice, 'id')
                label = "번역"
                style = discord.ButtonStyle.secondary
        except Exception as e:
            print(e)
        finally:
            super().__init__(label=label, style=style, custom_id=custom_id)
            self.notice = notice


    async def callback(self, interaction: discord.Interaction):
        try:
            id= interaction.data['custom_id']
            if id.startswith('1'):
                print('add_sch_button')
                print(self.notice.applyHeadDate, self.notice.applyTailDate)
                await create_event(self.notice)
                await interaction.response.send_message("add_sch_button")
            elif id.startswith('2'):
                print('trans_button')
                await interaction.response.send_message("trans_button")
        except Exception as e:
            print(e)
        finally:
            pass