from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ledger.api.serializers import LedgerSerializer
from ledger.models import Ledger
from utils import error_messages


class LedgerViewSet(ModelViewSet):
    serializer_class = LedgerSerializer
    model = Ledger
    queryset = Ledger.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(
            {"result": True, "data": serializer.data}, status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None, *args, **kwargs):
        user = request.user
        ledger = get_object_or_404(Ledger, id=pk)
        if ledger.user != user:
            raise ValidationError(error_messages.NOT_WRITER, code="NOT_WRITER")
        if not ledger.is_active:
            raise ValidationError(
                error_messages.LEDGER_IS_NOT_ACTIVE, code="LEDGER_IS_NOT_ACTIVE"
            )
        serializer = self.serializer_class(ledger, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"result": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None, *args, **kwargs):
        user = request.user
        ledger = get_object_or_404(Ledger, id=pk)
        if ledger.user != user:
            raise ValidationError(error_messages.NOT_WRITER, code="NOT_WRITER")
        if not ledger.is_active:
            raise ValidationError(
                error_messages.LEDGER_IS_NOT_ACTIVE, code="LEDGER_IS_NOT_ACTIVE"
            )
        ledger.is_active = False
        ledger.save()

        return Response(
            {"result": True, "data": self.serializer_class(instance=ledger).data},
            status=status.HTTP_200_OK,
        )
