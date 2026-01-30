import asyncio
from pyspapi import SPAPI

spapi = SPAPI(card_id="CARD_ID", token="TOKEN")



async def main():
    new_balance = await spapi.create_transaction(
        receiver="20199", amount=1, comment="test"
    )
    print(new_balance)


asyncio.run(main())
