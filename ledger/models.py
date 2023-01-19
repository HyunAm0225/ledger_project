from django.db import models

from base.models import BaseModel


class Ledger(BaseModel):
    memo = models.TextField(verbose_name="메모", default=None, null=True)
    amount = models.BigIntegerField(verbose_name="예산", default=0)
    user = models.ForeignKey(
        verbose_name="유저",
        to="user.User",
        on_delete=models.CASCADE,
        related_name="ledger",
    )
    is_active = models.BooleanField(verbose_name="활성화 여부", default=True)

    class Meta:
        verbose_name = "가계부"
