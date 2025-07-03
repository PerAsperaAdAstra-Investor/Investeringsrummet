import stripe
from flask import Flask, request, jsonify

app = Flask(__name__)

# Din Stripe webhook secret (hämta från Stripe Dashboard)
endpoint_secret = "whsec_XXXXX"

# Sätt din Stripe API-nyckel
stripe.api_key = "***REMOVED***ubsH6Q9qX3CK0Fex69CJUUfID2fYcw48M6W2QBhASxnDpOkIGfTnVu7zozyizV0x0U1bwU7vX9MdlUa8E00teSbfDDG"

@app.route("/stripe_webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except stripe.error.SignatureVerificationError:
        return jsonify({"error": "Invalid signature"}), 400

    # Hantera eventet
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = session.get("customer_email")

        # ➕ Här sätter du användaren som premium i din databas
        print(f"Premium-användare: {customer_email}")

    return jsonify(success=True)