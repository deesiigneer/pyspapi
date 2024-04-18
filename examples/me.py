from pyspapi import SPAPI
from asyncio import get_event_loop

spapi = SPAPI(card_id='CARD_ID', token='TOKEN')


async def main():
    me = await spapi.me
    print(me)

loop = get_event_loop()
loop.run_until_complete(main())
