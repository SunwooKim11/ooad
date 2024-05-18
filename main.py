import discord
from discord.ext import commands
from controller import Controller
from dico_token import KEY
from notice import *
from button import MyButton

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)
controller = Controller()

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    await client.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))

@client.command()
async def keyword(ctx, *args):
    if len(args) == 0:
        await ctx.send("공지사항을 검색할 키워드를 입력해주세요.")
    else:
        arg = ' '.join(args)
        print(arg)
        await send_notice(ctx=ctx, scheduled=False, trans=False, keyword=arg, uid=None)

async def send_notice(ctx, scheduled=False, trans=False, keyword=None, uid=None):
    notice = CheckInNotice(
        title='2024년도 기숙사 신입생 모집 공고',
        target='2024년도 신입생',
        applyDate='2024.06.03.(수) 11:00 ~ 2024.06.09.(화) 13:00',
        acceptDate='2024.01.15',
        payDate='2024.01.20 ~ 2024.01.25',
        url='https://dormitory.kookmin.ac.kr/notice/notice/509'
    )

    embed = discord.Embed(title=notice.title, url=notice.url, color=0x00ff00)
    attr = ['target', 'applyDate', 'acceptDate', 'payDate']

    if trans:
        header = ['Who to apply for', 'Application period', 'Date of announcement of acceptance', 'Living fee payment period']
    else:
        header = ['신청대상', '신청기간', '합격발표일자', '관비납부기간']

    for i in range(len(header)):
        embed.add_field(name=header[i], value=getattr(notice, attr[i]), inline=False)

    view = discord.ui.View()
    view.add_item(MyButton(kind='add_sch_button', notice=notice))
    
    await ctx.send(embed=embed, view=view)

@client.event
async def new_notice():
    pass

if __name__ == '__main__':
    client.run(KEY)
