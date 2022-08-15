import pyspapi
import asyncio


api = pyspapi.API(card_id='card_id', token='token')


async def main():
    user = await api.get_user(264329096920563714)
    print(user)
    print(user.access)
    # У API есть лимиты, каждый user = 1 запрос, учитывайте это при использовании get_users
    # https://spworlds.readthedocs.io/ru/latest/index.html#id3
    users = await api.get_users([262632724928397312, 264329096920563714])
    for user in users:
        print(user)
        if user is not None:
            print(user.access)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
