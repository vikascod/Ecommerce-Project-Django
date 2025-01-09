def not_authenticated(user):
    return not user.is_authenticated