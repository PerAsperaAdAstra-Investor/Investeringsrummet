
import pyrebase
firebaseConfig = {
  "apiKey": "AIzaSyCT1L6iQoWnC6k9gdWvse_apYRBozp1zHA",
  "authDomain": "investeringsrummet-3fe42.firebaseapp.com",
  "projectId": "investeringsrummet-3fe42",
  "storageBucket": "investeringsrummet-3fe42.appspot.com",
  "databaseURL": "https://investeringsrummet-3fe42.firebaseio.com",
  "messagingSenderId": "478793442960",
  "appId": "1:478793442960:web:cafc4c6d22dbbf60ff5a15",
  "measurementId": "G-KF8X5TFSQ4"
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
