import discord
from discord.ext import commands
from controller import Controller
import datetime
from dico_token import KEY

CHANNEL_ID = '<CHANNEL_ID>'
EMAIL = 'seoun2001@kookmin.ac.kr'
COMMAND_LIST= """
1. !keyword (word):
- 제목에 'word'를 포함한 공지를 올려드립니다. 
2. !trans (uid):
- 'uid'에 있는 공지사항 내용을 번역해서 유저에게 보냅니다.
3. !ques:
- admin의 email을 돌려줍니다.
4. !help:
- 가능한 명령어를 출력합니다. 
5. !sch (uid):
- 'uid'의 공지사항 일정을 디스코드 이벤트에 추가합니다.
"""
testData = {
    'title': '2024년도 기숙사 신입생 모집 공고 ',
    'target': '2024년도 신입생',
    'applyDate': '2024.01.01 ~ 2024.01.10',
    'acceptDate': '2024.01.15',
    'payDate': '2024.01.20 ~ 2024.01.25',
    'url': 'https://dormitory.kookmin.ac.kr/notice/notice/509'
}
 
 
class MyClient(discord.Client):
    async def send_notice(message, scheduled=False, trans=False, keyword=None, uid=None):
        # notice controller.get_notice(keyword=arg)
        notice= testData
        uid = notice['url'].split('/')[-1]

        embed = discord.Embed(title= notice['title'] , url = notice['url'], color=0x00ff00)
        attr = ['title', 'target', 'applyDate', 'acceptDate', 'payDate']

        if trans:
            header = ['Who to apply for', 'Application period', 'Date of announcement of acceptance', 'Living fee payment period']
        else:
            header = ['신청대상', '신청기간', '합격발표일자', '관비납부기간']

        for i in range(len(header)):
            embed.add_field(name=header[i], value=notice[attr[i]], inline=False)

        # 버튼 생성
        add_sch_button = discord.ui.Button(label='일정추가', style=discord.ButtonStyle.primary, custom_id='add_sch_button-{uid}', )
        trans_button = discord.ui.Button(label='번역', style=discord.ButtonStyle.secondary, custom_id='trans_button-{uid}', disabled=trans)
        view = discord.ui.View()
        view.add_item(add_sch_button)
        view.add_item(trans_button)

        await message.channel.send(embed=embed, view=view)


    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))
 
    async def on_message(self, message):
        if message.author == self.user:
            return
 
        if message.content == 'ping':
            await message.channel.send('pong {0.author.mention}'.format(message))
        elif message.content.startswith('!keyword'):
            await send_notice(message=interaction.message, scheduled = False, trans = False, keyword = None, uid = None)

    # 버튼 클릭 이벤트 핸들러
    async def on_interaction(self, interaction: discord.Interaction):
        btn_id = interaction.data['custom_id'].split('-')
        # await interaction.response.send_message('{}이 클릭되었습니다!'.format(interaction.data['custom_id'] ), ephemeral=True)
        if btn_id[0] == 'add_sch_button':
            pass
        elif btn_id[0]== 'trans_button':
            await self.send_notice(message=interaction.message, scheduled = False, trans = True, keyword = None, uid = btn_id[1])

    
   
 
 
intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
controller = Controller()



 
if __name__ == '__main__':

    client.run(KEY)