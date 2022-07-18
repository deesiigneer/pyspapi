import pyspapi

spapi = pyspapi.SPAPI(card_id='card_id', token='token')

print(spapi.payment(amount=1,
                    redirect_url='https://www.google.com/',
                    webhook_url='https://www.google.com/',
                    data='some-data'
                    )
      )
