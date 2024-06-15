import json
import aiohttp
import asyncio

from notice import *
from discord_info import TOKEN, GUILD_ID, CHANNEL_ID
# ref 
# 올바른 코드 : https://github.com/Fortex365/Barmaid/blob/main/barmaid/events/scheduled_events.py
# 원본 글: https://gist.github.com/adamsbytes/8445e2f9a97ae98052297a4415b5356f
class DiscordEvents:
    '''Class to create and list Discord events utilizing their API'''
    def __init__(self, discord_token: str, guild_id: str) -> None:
        self.guild_id = guild_id
        
        # VOICE 채널이면 2, 그렇지않으면 3
        # VOICE 채널으로 설정안해도 되므로 channel_id는 None으로 설정
        self.EXTERNAL = 3
        self.EVENT_PRIVACY_LEVEL = 2

        self.channel_id = None

        self.base_api_url = 'https://discord.com/api/v10'
        self.auth_headers = {
            'Authorization': f'Bot {discord_token}',
            'User-Agent': f'DiscordBot (https://discord.com/oauth2/authorize?client_id=1239072859746472058&permissions=8&scope=bot) Python/3.11 aiohttp/3.9.5',
            'Content-Type': 'application/json'
        }

    async def list_guild_events(self) -> list:
        '''Returns a list of upcoming events for the supplied guild ID
        Format of return is a list of one dictionary per event containing information.'''
        event_retrieve_url = f'{self.base_api_url}/guilds/{self.guild_id}/scheduled-events'
        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            try:
                async with session.get(event_retrieve_url) as response:
                    response.raise_for_status()
                    assert response.status == 200
                    response_list = json.loads(await response.read())
            except Exception as e:
                print(f'EXCEPTION: {e}')
            finally:
                await session.close()
        return response_list
        
   
    async def create_guild_event(self, notice):
        '''Creates a guild event using the supplied arguments
        The expected event_metadata format is event_metadata={'location': 'YOUR_LOCATION_NAME'}
        The required time format is %Y-%m-%dT%H:%M:%S'''

        event_create_url = f'{self.base_api_url}/guilds/{self.guild_id}/scheduled-events'
    
        event_data = json.dumps({
            'name': notice.title,
            'scheduled_start_time': notice.eventHeadDate,
            'scheduled_end_time': notice.eventTailDate,
            'description': notice.get_content(),
            'entity_metadata': {'location': 'Online'},
            'privacy_level': self.EVENT_PRIVACY_LEVEL,
            'channel_id': self.channel_id,
            'entity_type': self.EXTERNAL
        })

        print("Sending data: ", event_data)  # 디버그용: 요청 데이터를 출력합니다.

        async with aiohttp.ClientSession(headers=self.auth_headers) as session:
            try:
                async with session.post(event_create_url, data=event_data) as response:
                    if response.status != 200:
                        print(f'EXCEPTION: {response.status}, response: {await response.text()}')  # 예외 발생 시 응답 본문을 출력합니다.
                    response.raise_for_status()
            except Exception as e:
                print(f'EXCEPTION: {e}')
            finally:
                await session.close()

async def create_event(notice):
    event = DiscordEvents(TOKEN, GUILD_ID)


    await event.create_guild_event(notice)

if __name__ == "__main__":
    asyncio.run(create_event())
