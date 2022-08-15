import pyspapi
import asyncio

api = pyspapi.API(card_id='CARD_ID', token='TOKEN')


async def main():
    print(await api.transaction(receiver=12345,
                                amount=1,
                                comment="test"
                                )
          )

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
