# THERE ARE TWO CODES. THE FIRST WORKS BY USING CLIENTS UID. THE SECOND ITS INDEXING ("User1" == user 1)

# -----------------------------------------------First_CODE-------------------------------------------------------------
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("accountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://parkingsystemdatabasefyp-default-rtdb.firebaseio.com/'
    })

# retrieve the specific user's data
userData = db.reference("Users").child("CUlZJySqV0SZWvLzNe0W8qKAEAF3").get()
# retrieve first name of user
print('User Selected: '+userData['firstName'])

# Fetching number plates, and exit dates.
print('Getting exit dates along with number plates associated with '+userData['firstName'])

# retrieve all bookings for the user
allBookings = db.reference("Bookings").child("CUlZJySqV0SZWvLzNe0W8qKAEAF3").get()
# go through each booking and get number plates and date of exit
for key, value in allBookings.items():
    booking = value
    print('Number Plate: '+booking['numPlate']+'\tExit Date: '+booking['to'])

print("Program ended..........")


# ---------------------------------------------SECOND_CODE--------------------------------------------------------------

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
#
# cred = credentials.Certificate("accountKey.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL':'https://parkingsystemdatabasefyp-default-rtdb.firebaseio.com/'
#     })
#
# # retrieve all Users' arrayObject
# allData = db.reference("Users").get()
#
# # make user IDs' dictionary which contains all users' IDs
# users = {}
# c = 1
#
# for key, value in allData.items():
#     #user1 user2 user3.... this is key and value is User ID
#     users['user'+str(c)] = key
#     c += 1
#
# # retrieve one user's data
# userData = db.reference("Users").child(users.get('user2')).get()
# #can retrieve any information by putting its key just like given example below
# print('User Selected: '+userData['firstName'])
#
# # Fetching number plates, and exit dates. Because one user can have multiple bookings therefore
# # he may have 0 , 1 or more than 1 number plates and dates
# print('Getting exit dates along with number plates associated with '+userData['firstName'])
#
# # retrieve user1's all bookings
# allBookings = db.reference("Bookings").child(users['user1']).get()
# # go through each booking and get number plates and date of exit
# for key, value in allBookings.items():
#     booking = value
#     print('Number Plate: '+booking['numPlate']+'\tExit Date: '+booking['to'])
#
#
# print("Program ended..........")
