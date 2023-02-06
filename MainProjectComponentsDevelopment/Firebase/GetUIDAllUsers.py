import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("accountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://parkingsystemdatabasefyp-default-rtdb.firebaseio.com/',
    'storageBucket': 'parkingsystemdatabasefyp.appspot.com'
    })

# Retrieve all available user IDs
page = auth.list_users()
while page:
    for user in page.users:
        print('User UID:', user.uid)
    if not page.next_page_token:
        break
    page = auth.list_users(page.next_page_token)

