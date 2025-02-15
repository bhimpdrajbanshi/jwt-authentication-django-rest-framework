from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

class PhoneNumberBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, password=None):
        try:
            user = get_user_model().objects.get(Q(phone_number=phone_number))
            # Check if the provided password matches the stored hashed password
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
