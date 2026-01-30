import asyncio
from pyspapi import SPAPI

spapi = SPAPI(card_id="CARD_ID", token="TOKEN")


async def main():
    me = await spapi.me
    print(me)


asyncio.run(main())
