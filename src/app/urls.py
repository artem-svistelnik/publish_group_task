from django.contrib import admin
from django.urls import path, include

from account.views import index

urlpatterns = [
    path("", index, name="index"),
    path("admin/", admin.site.urls),
    path("account/", include("account.urls", namespace="account")),
    path(
        "data-aggregator/", include("data_aggregator.urls", namespace="data_aggregator")
    ),
]
