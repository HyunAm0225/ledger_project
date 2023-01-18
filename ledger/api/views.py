from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ledger.api.serializers import LedgerSerializer
from ledger.models import Ledger


class LedgerViewSet(ModelViewSet):
    serializer_class = LedgerSerializer
    model = Ledger
    queryset = Ledger.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save(user=user)
        return Response(
            {"result": True, "data": serializers.data}, status=status.HTTP_201_CREATED
        )
