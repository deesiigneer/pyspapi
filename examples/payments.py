import asyncio
from pyspapi import SPAPI
from pyspapi.types import Item

spapi = SPAPI(card_id="CARD_ID", token="TOKEN")


items = [
    Item("first item", 1, 2, "first item comment").to_json(),
    Item("second item", 3, 4, "second item comment").to_json(),
]


async def main():
    print(
        await spapi.create_payment(
            items=items,
            redirect_url="https://www.google.com/",
            webhook_url="https://www.google.com/",
            data="some-data",
        )
    )


asyncio.run(main())
