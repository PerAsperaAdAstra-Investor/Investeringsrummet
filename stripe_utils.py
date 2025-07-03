import stripe
from decouple import config

stripe.api_key = config("STRIPE_SECRET_KEY")

def create_checkout_session(user_email):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="subscription",
        line_items=[{
            "price": config("STRIPE_PRICE_ID"),
            "quantity": 1,
        }],
        success_url=config("STRIPE_SUCCESS_URL"),
        cancel_url=config("STRIPE_CANCEL_URL"),
        customer_email=user_email
    )
    return session.url