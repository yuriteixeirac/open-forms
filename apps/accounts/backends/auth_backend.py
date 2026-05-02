from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
from django.core.validators import validate_email, ValidationError
from apps.accounts.models import User
from typing import Optional


class AuthBackend(BaseBackend):
    def authenticate(
        self,
        request: Optional[HttpRequest],
        username: str | None = None,
        email: str | None = None,
        password: str | None = None
    ) -> User | None:     # type: ignore
        email = email or username

        if not (email):
            return

        try:
            validate_email(email)
        except ValidationError:
            return

        user: User = User.objects.filter(email=email).first()    # type: ignore

        if not user:
            return

        if not check_password(password, user.password):
            return

        return user


    def get_user(self, id: int) -> User | None:     # type: ignore
        try:
            return User.objects.filter(pk=id).first()   # type: ignore
        except User.DoesNotExist:   # type: ignore
            return
