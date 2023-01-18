from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from schema import And, Schema

from ledger.models import Ledger
from user.models import User


class LedgerApiTestCase(APITestCase):
    def refresh_access_token(self, client_user):
        access_token = self.client.post(
            self.login_url,
            {
                "email": client_user.email,
                "password": "test001!",
            },
        ).data.get("token")
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token['access_token']}"
        )

    @classmethod
    def setUpTestData(cls) -> None:
        super(LedgerApiTestCase, cls).setUpTestData()
        cls.factory = APIRequestFactory()
        cls.register_url = "/api/v1/users/register/"
        cls.login_url = "/api/v1/users/login/"
        cls.logout_url = "/api/v1/users/logout/"
        cls.ledger_url = "/api/v1/ledgers/"
        User.objects.create(email="test@test.com", password=make_password("test001!"))
        cls.test_user = User.objects.get(email="test@test.com")

    def setUp(self):
        self.refresh_access_token(self.test_user)

    def test_회계_작성(self):
        ledger_info_schema = Schema(
            {
                "id": And(int, lambda x: x > 0),
                "user": self.test_user.id,
                "memo": "hello",
                "amount": 15000,
                "created_at": And(str, len),
                "updated_at": And(str, len),
                "is_active": True,
            }
        )
        data = {"memo": "hello", "amount": 15000}
        res = self.client.post(self.ledger_url, data=data, format="json")

        response_schema = Schema(
            {
                "result": True,
                "data": ledger_info_schema,
            }
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        assert response_schema.validate(res.json())

    def test_회계_수정(self):
        self.test_회계_작성()
        ledger = Ledger.objects.all().first()
        ledger_info_schema = Schema(
            {
                "id": And(int, lambda x: x > 0),
                "user": self.test_user.id,
                "memo": "수정완료!",
                "amount": 7500,
                "created_at": And(str, len),
                "updated_at": And(str, len),
                "is_active": True,
            }
        )
        data = {"memo": "수정완료!", "amount": 7500}
        res = self.client.patch(
            f"{self.ledger_url}{ledger.pk}/", data=data, format="json"
        )

        response_schema = Schema(
            {
                "result": True,
                "data": ledger_info_schema,
            }
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        assert response_schema.validate(res.json())

    def test_회계_삭제(self):
        self.test_회계_작성()
        ledger = Ledger.objects.all().first()
        res = self.client.delete(f"{self.ledger_url}{ledger.pk}/", format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Ledger.objects.filter(is_active=False).count(), 1)
