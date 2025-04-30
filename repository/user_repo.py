from model.user import User

_user_store = {}


def save_user(user: User):
    _user_store[user.id] = user
    return True


def get_user(user_id: int) -> User:
    return _user_store.get(user_id)
