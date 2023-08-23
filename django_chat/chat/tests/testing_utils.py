from django.contrib.auth.models import User


def get_test_user() -> User:
    test_user = User(username="user")
    test_user.save()

    return test_user
