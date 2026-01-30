import asyncio
from pyspapi import SPAPI

spapi = SPAPI(card_id="CARD_ID", token="TOKEN")



async def main():
    user = await spapi.get_user(262632724928397312)
    print(user.username, user.uuid)
    for card in user.cards:
        print(card.name, card.number)


asyncio.run(main())
