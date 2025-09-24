import pymongo
dburl="mongodb+srv://rohithvaddepally:thegymstring@cluster0.nn6v2ug.mongodb.net/"
connection=pymongo.MongoClient(dburl)

projectdb=connection["THE_GYM_BYJOHNSON"]
user_data=projectdb["Users"]
admin_data=projectdb["Admin"]
payment_due=projectdb["payments"]
payment_history=projectdb["payment_history"]
offline_payments = projectdb["offline_payments"]
otp_storage=projectdb["others"]


async def get_user_by_email(email: str):
    user = user_data.find_one({"email": email})
    return user

# Determine membership based on amount
def get_membership_plan(amount):
    if amount == 900:
        return "Basic"
    elif amount == 1500:
        return "Premium"
    elif amount == 3500:
        return "Pro"
    else:
        return "NA"
    


