import pyspapi
import asyncio

api = pyspapi.API(card_id='card_id', token='token')


async def main():
    print(await api.payment(amount=1,
                            redirect_url='https://www.google.com/',
                            webhook_url='https://www.google.com/',
                            data='some-data'
                            )
          )

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
