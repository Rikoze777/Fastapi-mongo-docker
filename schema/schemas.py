def individual_user(user):
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "password": user["password"],
        "token": user["token"],
    }


def users_list(users):
    return [individual_user(user) for user in users]


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}