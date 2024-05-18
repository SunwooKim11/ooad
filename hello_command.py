class HelloCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='hello') # 그룹 명령어는 단독으로 호출할 수 없습니다.
    async def hello_group(self, ctx: discord.ext.commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send('그룹 명령어는 단독으로 실행될 수 없습니다.')

    @hello_group.command(name='korean')
    async def hello_korean(self, ctx):
        # !hello korean 명령어에 대한 응답을 처리합니다.
        await ctx.send('안녕하세요.')

    @hello_korean.error
    async def hello_korean_error(self, ctx, error):
        # 이곳에서 hello_korean 명령어의 오류를 처리합니다.
        await ctx.send(error)

    @hello_group.command(name='english')
    async def hello_english(self, ctx):
        # !hello english 명령어에 대한 응답을 처리합니다.
        await ctx.send('hello')
        
    @commands.command(name='hi') # 단일 명령어는 단독으로 호출합니다.
    async def hi(self, ctx):
        # !hi 명령어에 대한 응답을 처리합니다.
        await ctx.send('hi')

    @commands.command(name='hii') # 명령어 외에 인자를 받을 수 있습니다.
    async def hi_args(self, ctx, *args):
        # args는 튜플 형태로 받습니다.