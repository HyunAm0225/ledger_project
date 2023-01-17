from rest_framework.test import APITestCase, APIRequestFactory


class UserApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super(UserApiTestCase, cls).setUpTestData()
        cls.factory = APIRequestFactory()
        cls.register_url = "/api/v1/users/register/"

    def test_유저_회원가입(self):
        data = {
            "email": "test@test.com",
            "password": "test123!",
        }
        res = self.client.post(self.register_url, data=data, format="json")
        print(res.json())
