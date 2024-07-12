import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./config/firebase_credentials.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
