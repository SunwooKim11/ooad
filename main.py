import discord
from discord.ext import commands, tasks
from controller import Controller
from discord_info import TOKEN, GUILD_ID, CHANNEL_ID
from notice_model import CheckInNotice
from discord_component_creator import DiscordComponentCreator
import time 

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)
controller = Controller()
dcc= DiscordComponentCreator()

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    guild = discord.utils.get(client.guilds, id=int(GUILD_ID))
    channel = discord.utils.get(guild.text_channels, id=int(CHANNEL_ID))
    # Start checking new notices
    send_new_notice.start(channel)

@tasks.loop(minutes=5)
async def send_new_notice(ctx):
    new_url_id = await controller.check_new_notice()
    print(new_url_id)
    if new_url_id != -1:
        await send_msg(ctx_or_interaction=ctx, lang='ko', keyword=None, url_id=new_url_id)
    else:
        pass

@client.command()
async def keyword(ctx, *args):
    begin = time.time()
    if len(args) == 0:
        await ctx.send("공지사항을 검색할 키워드를 입력해주세요.")
    else:
        arg = ' '.join(args)
        print(arg)
        await send_msg(ctx_or_interaction=ctx, lang='ko', keyword=arg, url_id=None)
        end = time.time()
        print("키워드 공지 발송 시간(sec): ", end - begin)

@client.command()
async def ques(ctx):
    begin = time.time() 
    await ctx.send(controller.get_email())
    end = time.time()
    print("이메일 발송 시간(sec): ", end - begin)


async def send_msg(ctx_or_interaction, lang='ko', keyword=None, url_id=None):
    try:
        if keyword == "test":
            notice = CheckInNotice("test_title", "test_target", "2025.05.30.(목) 11:00 ~ 2025.06.06.(목)" , "2025.06.07.(금) 15:00", 
            "2025.06.07.(금) 15:00 ~ 2025.06.11.(화) 23:30", "https://dormitory.kookmin.ac.kr/notice/notice/530", ['신청대상', '신청기간', '합격발표', '납부기간'])
        else:
            notice = controller.get_notice(keyword, url_id, lang)
    
        print(type(notice))
        view, embed = controller.get_discord_component(notice, send_msg)
        
        if isinstance(ctx_or_interaction, discord.Interaction):
            print('interaction')
            await ctx_or_interaction.response.send_message(embed=embed, view=view)
        else:
            await ctx_or_interaction.send(embed=embed, view=view)
    except Exception as e:
        print(e)
        await ctx_or_interaction.send("Error occurred while sending message.")


if __name__ == '__main__':
    client.run(TOKEN)