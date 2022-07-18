import pyspapi

spapi = pyspapi.SPAPI(card_id='card_id', token='token')

print(spapi.get_user(262632724928397312))

print(spapi.get_user(262632724928397312).username)

print(spapi.get_user(262632724928397312).access)

print(spapi.get_users([262632724928397312, 264329096920563714]))
