import pyspapi

spapi = pyspapi.SPAPI(card_id='CARD_ID', token='TOKEN')

print(spapi.transaction(receiver=12345,
                        amount=1,
                        comment="test"
                        )
      )
