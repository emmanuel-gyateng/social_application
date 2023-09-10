"""Test cases for authentication application"""
import os
import pdb
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from authentications.models import Users


# Create your tests here.
class TestSetup(APITestCase):
    """Setup class for the test cases"""

    def setUp(self):
        """Setup of the test"""
        self.register_url = "/account/register/"
        self.login_url = "/account/login/"
        self.logout_url = "/account/logout/"
        self.google_url = "/account/google/"
        self.change_password_url = "/account/change-password/"
        self.admin_register_url = "/account/register-admin/"
        self.user = Users.objects.create_superuser(
            username="admin", email_address="admin@admin.com", password="admin1234"
        )
        self.token = RefreshToken.for_user(self.user)
        self.refresh_token = str(self.token)
        return super().setUp()


class TestUserRegistration(TestSetup):
    """Api test for user registration"""

    def test_user_can_register(self):
        """Test to see if user can register"""
        register_url = self.register_url
        data = {
            "full_name":"gull_name_tria",
            "email_address": "test1@gmail.com",
            "username": "test1",
            "password": "test1234",
        }
        response = self.client.post(register_url, data, format="json")

        # pdb.set_trace()
        self.assertEqual(response.status_code, 201)


class TestUserLogin(TestSetup):
    """Api test for user login"""

    def test_not_active_or_not_registered_user_cannot_login(self):
        """Test to check that users that are not active or not registered
        can not login into the system"""
        res = self.client.post(
            self.login_url,
            {
                "email_address": "test1@gmail.com",
                "password": "test1234",
            },
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_active_and_validated_users_can_login(self):
        """Test to see if user that is not active or not registered
        ca login into the system"""
        user_email = "admin@admin.com"
        user_password = "admin1234"
        res = self.client.post(
            self.login_url,
            {"email_address": user_email, "password": user_password},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_logout(self):
        """Test users can logout successful"""
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(self.token.access_token)
        )
        response = self.client.post(
            self.logout_url, {"refresh_token": self.refresh_token}, format="json"
        )
        # pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)


class ChangeUserPassword(TestSetup):
    """Change password API endpoint test cases"""

    def test_users_can_change_password(self):
        """Test to check if authenticated users can change their password"""
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + str(self.token.access_token)
        )
        response = self.client.patch(
            self.change_password_url,
            {"old_password": "admin1234", "new_password": "newPassword123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_users_can_not_change_paswword(self):
        """Test to test if unauthenticated user can change their password"""
        self.client.force_authenticate(user=None)
        response = self.client.patch(
            self.change_password_url,
            {"old_password": "admin1234", "new_password": "newPassword123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
