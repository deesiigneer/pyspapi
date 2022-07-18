import pyspapi

spapi = pyspapi.SPAPI(card_id='your_card_id', token='your_token')

print(spapi.webhook_verify(data='webhook_data', header='webhook_header'))
