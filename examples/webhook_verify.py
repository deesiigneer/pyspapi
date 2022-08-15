import pyspapi
import asyncio

api = pyspapi.API(card_id='your_card_id', token='your_token')

async def main():
    print(await api.webhook_verify(data='webhook_data', header='webhook_header'))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
