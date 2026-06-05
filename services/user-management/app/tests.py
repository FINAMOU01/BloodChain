from django.test import TestCase
from .models import User, Token


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="donor@test.com",
            password="secret123",
            first_name="John",
            last_name="Doe",
            role="donor",
        )
        assert user.email == "donor@test.com"
        assert user.role == "donor"
        assert user.is_active is True
        assert str(user) == "donor@test.com"

    def test_create_user_without_email_raises(self):
        import pytest
        with pytest.raises(ValueError, match="Email is required"):
            User.objects.create_user(email="", password="secret")

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email="admin@test.com", password="admin123"
        )
        assert admin.role == "admin"

    def test_user_default_role_is_donor(self):
        user = User.objects.create_user(email="new@test.com", password="pass")
        assert user.role == "donor"


class TokenModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="tok@test.com", password="pass")

    def test_create_token(self):
        token = Token.objects.create(user=self.user, token="abc123")
        assert str(token) == "Token for tok@test.com"
        assert token.token == "abc123"
