import pyspapi

spapi = pyspapi.SPAPI(card_id='card_id', token='token').balance

print(spapi.check_users_access([262632724928397312, 264329096920563714]))
