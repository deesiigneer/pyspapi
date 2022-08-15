import pyspapi

api = pyspapi.API(card_id='your_card_id', token='your_token')

api.listener(host='myhost.com', port=80, webhook_path='/webhook/')