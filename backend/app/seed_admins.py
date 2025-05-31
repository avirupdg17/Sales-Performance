import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.db import SalesDB

users_to_seed = [
    # Admin users
    {
        "name": "Admin One",
        "photo": None,
        "username": "admin1",
        "password": "adminpass1",
        "role": "Admin",
        "email": "admin1@example.com",
        "phone": "9999999999"
    },
    {
        "name": "Admin Two",
        "photo": None,
        "username": "admin2",
        "password": "adminpass2",
        "role": "Admin",
        "email": "admin2@example.com",
        "phone": "8888888888"
    },

    # Regular users
    {
        "name": "Swagat Patel",
        "photo": None,
        "username": "swagatp",
        "password": "7978650309",
        "role": "ASC",
        "email": "",
        "phone": "7978650309"
    },
    {
        "name": "Aastik Das Gupta",
        "photo": None,
        "username": "aastikd",
        "password": "9876544321",
        "role": "ASC",
        "email": "",
        "phone": "9876544321"
    },
    {
        "name": "Rahul Batavia",
        "photo": None,
        "username": "rahulb",
        "password": "9876544322",
        "role": "ASC",
        "email": "",
        "phone": "9876544322"
    },
    {
        "name": "Krish Hablani",
        "photo": None,
        "username": "krishh",
        "password": "9876544323",
        "role": "Distributor",
        "email": "",
        "phone": "9876544323"
    },
    {
        "name": "Rajat Jain",
        "photo": None,
        "username": "rajatj",
        "password": "9876544324",
        "role": "ASC",
        "email": "",
        "phone": "9876544324"
    },
    {
        "name": "Trisha Upadhyay",
        "photo": None,
        "username": "trishau",
        "password": "9876544325",
        "role": "ASC",
        "email": "",
        "phone": "9876544325"
    },
    {
        "name": "Mansi Sharma",
        "photo": None,
        "username": "mansis",
        "password": "9876544326",
        "role": "ASC",
        "email": "",
        "phone": "9876544326"
    },
    {
        "name": "Amartya Sharma",
        "photo": None,
        "username": "amartyas",
        "password": "9876544327",
        "role": "ASC",
        "email": "",
        "phone": "9876544327"
    },
    {
        "name": "Arnav Okhade",
        "photo": None,
        "username": "arnavo",
        "password": "9876544328",
        "role": "ASC",
        "email": "",
        "phone": "9876544328"
    },
    {
        "name": "Mahesh Manda",
        "photo": None,
        "username": "maheshm",
        "password": "9876544329",
        "role": "ASC",
        "email": "",
        "phone": "9876544329"
    }
]


def seed_users():
    with SalesDB() as db:
        for user in users_to_seed:
            existing = db.get_records("users", [("phone", "=", user["phone"])])
            if not existing:
                db.add_record("users", user)
                print(f"Added user: {user['name']}")
            else:
                existing_user = existing[0]
                if existing_user["role"] != user["role"]:
                    db.update_records("users", [("phone", "=", user["phone"])], {"role": user["role"]})
                    print(f"Updated role for user: {user['name']} to {user['role']}")
                else:
                    print(f"User {user['name']} already exists with correct role.")


if __name__ == "__main__":
    seed_users()
