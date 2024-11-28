from django.urls import path
from data_aggregator.views import *

app_name = "data_aggregator"

urlpatterns = [
    path("upload/", upload_file, name="upload"),
    path("summary/", summary, name="summary"),
]
