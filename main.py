import discord
from discord.ext import commands
from controller import Controller
import datetime
from dico_token import KEY
# 

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


intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix = '!', intents=intents)
controller = Controller()

# decorator 문법

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    await client.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))

@client.command()
async def hello(ctx):
    await ctx.send('hello')

@client.command()
async def keyword(ctx, *args):
    if len(args) == 0:
        await ctx.send("공지사항을 검색할 키워드를 입력해주세요.")
    else:
        arg = args[1:]
        print(arg)
        await send_notice(ctx=ctx, scheduled=False, trans=False, keyword = arg, uid = None)

# 버튼 클릭 이벤트 핸들러
@client.event
async def on_interaction(interaction: discord.Interaction):
    message_content = interaction.message.content
    btn_id = interaction.data['custom_id'].split('-')
    # await interaction.response.send_message('{}이 클릭되었습니다!'.format(interaction.data['custom_id'] ), ephemeral=True)
    if btn_id[0] == 'add_sch_button':
        pass
    elif btn_id[0]== 'trans_button':
        await send_notice(ctx=interaction.context, scheduled = False, trans = True, keyword = None, uid = btn_id[1])


async def send_notice(ctx, scheduled=False, trans=False, keyword=None, uid=None):
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

    await ctx.send(embed=embed, view=view)

@client.event
async def new_notice():
    pass
    # BE에서 새로운 공지사항을 받아올 때마다 실행되는 함수



# @client.command() 
# async def trans(ctx, *args):   
#     if len(args) == 0:
#         await ctx.send("번역할 공지사항의 uri를 입력해주세요.")
#     else:
#         uid = args[0]
#         await ctx.send(controller.get_notice(uid=uid))

# @client.command()
# async def sch(ctx, *args):
#     await ctx.send('일정을 추가합니다.')
# @client.command()
# async def ques(ctx):
#     await ctx.send("다음 주소로 메일을 보내주시길 바랍니다\n{}.".format(EMAIL)) 

# @client.command()
# async def help(ctx):
#     await ctx.send(COMMAND_LIST)    


 
if __name__ == '__main__':

    client.run(KEY)