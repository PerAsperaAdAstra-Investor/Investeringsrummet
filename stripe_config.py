import stripe

stripe.api_key = "***REMOVED***ubsH6Q9qX3CK0Fex69CJUUfID2fYcw48M6W2QBhASxnDpOkIGfTnVu7zozyizV0x0U1bwU7vX9MdlUa8E00teSbfDDG"  # Lägg in din secret key

def create_checkout_session(user_email):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "sek",
                    "product_data": {
                        "name": "Investeringsrummet Premium",
                    },
                    "unit_amount": 4900,  # i öre = 49 kr
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="https://investeringsrummet-hgpif78s8wbgvkvdg3zqzz.streamlit.app?success=true",
        cancel_url="https://investeringsrummet-hgpif78s8wbgvkvdg3zqzz.streamlit.app?canceled=true",
        customer_email=user_email,
    )
    return session.url
