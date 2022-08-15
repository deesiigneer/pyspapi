import pyspapi

import pyspapi
import asyncio

api = pyspapi.API(card_id='card_id', token='token')


async def main():
    uuid = await pyspapi.API(card_id='card_id', token='token').get_uuid(username='deesiigneer')
    print(uuid)
    print(uuid.id, uuid.name)
    print(await pyspapi.API(card_id='card_id', token='token').get_uuids(['deesiigneer', '5opka', 'OsterMiner']))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

