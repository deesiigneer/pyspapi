import pyspapi
import asyncio

api = pyspapi.API(card_id='card_id', token='token')


async def main():
    mojang_profile = await api.get_profile(uuid='63ed47877aa3470fbfc46c5356c3d797')
    print(mojang_profile)
    print(mojang_profile.id, mojang_profile.timestamp)
    print(mojang_profile.skin, mojang_profile.skin.model, mojang_profile.skin.cape_url, mojang_profile.skin.url)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

