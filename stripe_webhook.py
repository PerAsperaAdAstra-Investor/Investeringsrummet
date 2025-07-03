from dotenv import load_dotenv
import os

if os.getenv("FLASK_ENV") != "production":
    load_dotenv()

import stripe
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Stripe Webhook Server is running!"

# Din Stripe webhook secret (hämta från Stripe Dashboard)
endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

# Sätt din Stripe API-nyckel
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

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


