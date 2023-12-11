def individual_serial(user):
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "password": user["password"],
        "token": user["token"],
    }


def list_serial(users):
    return [individual_serial(user) for user in users]
