from pyspapi import SPAPI
from asyncio import get_event_loop

spapi = SPAPI(card_id='CARD_ID', token='TOKEN')


async def main():
    new_balance = await spapi.create_transaction(receiver='77552',
                                                 amount=1,
                                                 comment="test"
                                                 )
    print(new_balance)


loop = get_event_loop()
loop.run_until_complete(main())
