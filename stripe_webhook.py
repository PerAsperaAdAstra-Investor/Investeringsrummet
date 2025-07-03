from dotenv import load_dotenv
import os
import pyrebase

if os.getenv("FLASK_ENV") != "production":
    load_dotenv()

import stripe
from flask import Flask, request, jsonify


firebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
}

firebase = pyrebase.initialize_app(firebase_config)
db = firebase.database()

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

        # ➕ Uppdatera användarens account_type till "premium"
        try:
            users = db.child("users").order_by_child("email").equal_to(customer_email).get()
            for user in users.each():
                db.child("users").child(user.key()).update({"account_type": "premium"})
                print(f"Updated {customer_email} to premium")
        except Exception as e:
            print(f"Failed to update user: {e}")

    return jsonify(success=True)


