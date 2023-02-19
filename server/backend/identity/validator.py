def validate_user_is_authenticated(user):
    if user.is_anonymous:
        raise Exception('Not authenticated')