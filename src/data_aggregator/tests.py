import pytest
from django.urls import reverse
from data_aggregator.models import File, DataRow
from io import StringIO
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_upload_file(client):
    user = User.objects.create_user(username="testuser", password="password123")
    client.login(username="testuser", password="password123")

    csv_file = StringIO(
        """
Advertiser,Brand,Start,End,Format,Platform,Impr
Samsung,SAMSUNG,01.04.2021,30.04.2021,Banner,facebook&instagram,5116431
    """
    )
    csv_file.name = "test.csv"

    response = client.post(reverse("data_aggregator:upload"), {"file": csv_file})

    assert response.status_code == 200

    assert File.objects.count() == 1
    assert DataRow.objects.count() == 1


@pytest.mark.django_db
def test_summary_view(client):
    user = User.objects.create_user(username="testuser", password="password123")
    client.login(username="testuser", password="password123")

    file = File.objects.create(upload_by=user, file_name="test.csv", status=True)
    DataRow.objects.create(
        file=file,
        advertiser="Samsung",
        brand="SAMSUNG",
        start_date="2021-04-01",
        end_date="2021-04-30",
        format="Banner",
        platform="facebook&instagram",
        impr=5116431,
    )

    response = client.get(reverse("data_aggregator:summary"))

    assert response.status_code == 200
    assert "summary_data" in response.context
