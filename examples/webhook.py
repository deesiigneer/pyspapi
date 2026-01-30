import asyncio
from pyspapi import SPAPI

spapi = SPAPI(card_id="CARD_ID", token="TOKEN")

# print(spapi.webhook_verify(data='webhook_data', header='webhook_header'))


async def main():
    print(await spapi.update_webhook(url="https://example.com/webhook"))


asyncio.run(main())
