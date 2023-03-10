from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from schema import And, Schema


class UserApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super(UserApiTestCase, cls).setUpTestData()
        cls.factory = APIRequestFactory()
        cls.register_url = "/api/v1/users/register/"
        cls.login_url = "/api/v1/users/login/"
        cls.logout_url = "/api/v1/users/logout/"

    def test_유저_회원가입_성공(self):
        token_info_schema = Schema(
            {
                "access_token": And(str, len),
                "refresh_token": And(str, len),
                "expires_at": And(int, lambda x: x > 0),
            }
        )
        user_info_schema = Schema(
            {
                "id": And(int, lambda x: x > 0),
                "email": And(str, len),
                "created_at": And(str, len),
                "updated_at": And(str, len),
            }
        )
        response_schema = Schema(
            {
                "token": token_info_schema,
                "user": user_info_schema,
            }
        )
        data = {
            "email": "test@test.com",
            "password": "test123!",
        }
        res = self.client.post(self.register_url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        assert response_schema.validate(res.json())

    def test_로그인_성공(self):
        self.test_유저_회원가입_성공()
        data = {
            "email": "test@test.com",
            "password": "test123!",
        }

        token_info_schema = Schema(
            {
                "access_token": And(str, len),
                "refresh_token": And(str, len),
                "expires_at": And(int, lambda x: x > 0),
            }
        )
        user_info_schema = Schema(
            {
                "id": And(int, lambda x: x > 0),
                "email": And(str, len),
                "created_at": And(str, len),
                "updated_at": And(str, len),
            }
        )
        response_schema = Schema(
            {
                "token": token_info_schema,
                "user": user_info_schema,
            }
        )
        res = self.client.post(self.login_url, data=data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        assert response_schema.validate(res.json())

    def test_로그아웃(self):
        self.test_유저_회원가입_성공()
        data = {
            "email": "test@test.com",
            "password": "test123!",
        }
        res = self.client.post(self.login_url, data=data, format="json")
        refresh_token = res.json()["token"].get("refresh_token")
        access_token = res.json()["token"].get("access_token")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        logout_data = {"refresh": refresh_token}
        res = self.client.post(self.logout_url, data=logout_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()["result"], True)
        re_logout_res = self.client.post(
            self.logout_url, data=logout_data, format="json"
        )
        self.assertEqual(re_logout_res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(re_logout_res.json()["error"], "AUTH_LOGOUT_FAILED")
