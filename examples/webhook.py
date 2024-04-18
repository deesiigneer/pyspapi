from pyspapi import SPAPI
from asyncio import get_event_loop

spapi = SPAPI(card_id='CARD_ID', token='TOKEN')

# print(spapi.webhook_verify(data='webhook_data', header='webhook_header'))


async def main():
    print(await spapi.update_webhook(url='https://example.com/webhook'))

loop = get_event_loop()
loop.run_until_complete(main())
