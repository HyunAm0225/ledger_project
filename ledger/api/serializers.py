from rest_framework import serializers

from ledger.models import Ledger


class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledger
        fields = [
            "id",
            "user",
            "amount",
            "memo",
            "created_at",
            "updated_at",
            "is_active",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }
