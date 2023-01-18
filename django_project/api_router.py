from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from ledger.api.views import LedgerViewSet
from user.api.views import AuthViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", AuthViewSet, basename="users")
router.register("ledgers", LedgerViewSet, basename="ledgers")

app_name = "api"
urlpatterns = router.urls
