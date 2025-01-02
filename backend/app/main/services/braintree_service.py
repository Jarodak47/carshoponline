import braintree
from app.main.core.config import Config
from app.main.models import Order,OrderVehicle

# Configuration de Braintree

class BrainTreeService:
    gateway = braintree.BraintreeGateway(
        braintree.Configuration(
            environment=Config.BRAINTREE_ENVIRONMENT,
            merchant_id=Config.BRAINTREE_MERCHANT_ID,
            public_key=Config.BRAINTREE_PUBLIC_KEY,
            private_key=Config.BRAINTREE_PRIVATE_KEY,
        )
    )

    def __init__(self):
        pass

    @classmethod
    async def generate_client_token(cls):
        response = cls.gateway.client_token.generate()
 
        print("token1234",response)
        return response
    
    @classmethod
    async def create_payment(cls, nonce,amount):
        response = cls.gateway.transaction.sale({
            "amount": amount,
            "payment_method_nonce": nonce,
            "options": {
                "submit_for_settlement": True
            }
        })


        print("response123",response)
        return response

braintree_api_service = BrainTreeService()
