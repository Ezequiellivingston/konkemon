users = [{"name": "bati","id":1},{"name": "cami","id":2},{"name": "gene","id":3}]

def get_users():
    return users


def get_users_one(id):
    user = next((u for u in users if u["id"] == id), None)
    return user