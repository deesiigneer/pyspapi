import pyspapi
import asyncio

api = pyspapi.API(card_id='card_id', token='token')


async def main():
    print(await api.get_name_history(uuid='63ed47877aa3470fbfc46c5356c3d797'))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

