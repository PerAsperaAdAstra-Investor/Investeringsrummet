from decouple import config
import pyrebase
firebaseConfig = {
    "apiKey": config("FIREBASE_API_KEY"),
    "authDomain": config("FIREBASE_AUTH_DOMAIN"),
    "projectId": config("FIREBASE_PROJECT_ID"),
    "storageBucket": config("FIREBASE_STORAGE_BUCKET"),
    "databaseURL": config("FIREBASE_DATABASE_URL"),
    "messagingSenderId": config("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": config("FIREBASE_APP_ID"),
    "measurementId": config("FIREBASE_MEASUREMENT_ID")
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
