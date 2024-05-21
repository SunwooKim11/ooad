import discord
from discord.ext import commands, tasks
from controller import Controller
from discord_info import TOKEN, GUILD_ID, CHANNEL_ID
from notice import *
from button import MyButton

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)
controller = Controller()

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))
    guild = discord.utils.get(client.guilds, id=int(GUILD_ID))
    channel = discord.utils.get(guild.text_channels, id=int(CHANNEL_ID))
    # Start checking new notices
    send_new_notice.start(channel)

@client.command()
async def keyword(ctx, *args):
    if len(args) == 0:
        await ctx.send("공지사항을 검색할 키워드를 입력해주세요.")
    else:
        arg = ' '.join(args)
        print(arg)
        await send_msg(ctx_or_interaction=ctx, lang='ko', keyword=arg, url_id=None)

@tasks.loop(minutes=1)
async def send_new_notice(ctx):
    new_url_id = await controller.new_notice()
    print(new_url_id)
    if new_url_id != -1:
        await send_msg(ctx_or_interaction=ctx, lang='ko', keyword=None, url_id=new_url_id)
    else:
        pass

@client.command()
async def ques(ctx):
    await ctx.send(Controller.get_email())

async def send_msg(ctx_or_interaction, lang='ko', keyword=None, url_id=None):
    notice = controller.get_notice(keyword, url_id, lang)
  
    print(type(notice))
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
    client.run(TOKEN)
