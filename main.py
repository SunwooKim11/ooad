import discord
from discord.ext import commands, tasks
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
    await client.change_presence(status=discord.Status.online)

@client.command()
async def keyword(ctx, *args):
    if len(args) == 0:
        await ctx.send("공지사항을 검색할 키워드를 입력해주세요.")
    else:
        arg = ' '.join(args)
        print(arg)
        await send_msg(ctx_or_interaction=ctx, lang='ko', keyword=arg, url_id=None)

@tasks.loop(hours=24)
async def send_new_notice(ctx):
    new_url_id = await controller.new_notice()
    if new_url_id != -1:
        await send_msg(ctx_or_interaction=ctx, lang='ko', keyword=None, url_id=new_url_id)

@client.command()
async def ques(ctx):
    await ctx.send(Controller.get_email())

async def send_msg(ctx_or_interaction, lang='ko', keyword=None, url_id=None):
    notice = await controller.get_notice(keyword, url_id, lang)
    # test code 
    # if(lang=='ko'):
    #     notice1 = CheckInNotice(
    #         title='2024년도 기숙사 신입생 모집 공고',
    #         target='2024년도 신입생',
    #         applyDate='2023.10.06.(목) 11시 ~ 10.12.(수) 13시',
    #         acceptDate='2024.01.15',
    #         payDate='2024.01.20 ~ 2024.01.25',
    #         url='https://dormitory.kookmin.ac.kr/notice/notice/509',
    #         header=['대상', '신청기간', '합격자 발표일', '입금기간']
    #     )
    #     notice2 = CheckOutNotice(
    #         title='2024-1학기 생활관 퇴실 및 호실이동 안내',
    #         target='교내-외 생활관 1학기 거주관생',
    #         outDate='2024.06.03.(수) 11:00 ~ 2024.06.09.(화) 13:00',
    #         moveDate='2024.06.03.(수) 11:00 ~ 2024.06.03.(수) 13:00',
    #         url='https://dormitory.kookmin.ac.kr/notice/notice/528',
    #         header=['대상', '퇴실기간', '호실이동']
    #     )
    # elif(lang=='en'):
    #     notice1 = CheckInNotice(
    #         title='2024 Dormitory New Student Recruitment Notice',
    #         target='New students in 2024',
    #         applyDate='2023.10.06.(목) 11시 ~ 10.12.(수) 13시',
    #         acceptDate='2024.01.15',
    #         payDate='2024.01.20 ~ 2024.01.25',
    #         url='https://dormitory.kookmin.ac.kr/notice/notice/509',
    #         header=['Target', 'Application Period', 'Successful Candidate Announcement Date', 'Deposit Period']
    #     )
    #     notice2 = CheckOutNotice(
    #         title='2024-1 Semester Life Center Exit and Room Movement Guide',
    #         target='Students living in the first semester of the in-school and out-of-school residence',
    #         outDate='2024.06.03.(Wed) 11:00 ~ 2024.06.09.(Thu) 13:00',
    #         moveDate='2024.06.03.(Wed) 11:00 ~ 2024.06.03.(Wed) 13:00',
    #         url='https://dormitory.kookmin.ac.kr/notice/notice/528',
    #         header=["Target", "Departure Period", "Moving to Room"]

    #     )
    # notice = notice1

    embed = get_embed(notice)
    view = discord.ui.View()
    view.add_item(MyButton(kind='add_sch_button', notice=notice, url_id=notice.get_id(), send_msg=send_msg))
    view.add_item(MyButton(kind='trans_button', notice=notice, url_id=notice.get_id(), send_msg=send_msg))

    if isinstance(ctx_or_interaction, discord.Interaction):
        print('interaction')
        await ctx_or_interaction.response.send_message(embed=embed, view=view)
    else:
        await ctx_or_interaction.send(embed=embed, view=view)

def get_embed(notice):
    embed = discord.Embed(title=notice.title, url=notice.url, color=0x00ff00)
    header = notice.header
    if isinstance(notice, CheckInNotice):
        attr = ['target', 'applyDate', 'acceptDate', 'payDate']
    elif isinstance(notice, CheckOutNotice):
        attr = ['target', 'outDate', 'moveDate']
    else:
        pass

    for i in range(len(header)):
        embed.add_field(name=header[i], value=getattr(notice, attr[i]), inline=False)

    return embed

if __name__ == '__main__':
    client.run(KEY)
