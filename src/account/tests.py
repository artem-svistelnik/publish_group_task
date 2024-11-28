import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_login(client):
    user = User.objects.create_user(username="testuser", password="password123")
    response = client.post(
        reverse("account:login"), {"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 302
    assert response.url == reverse("index")


@pytest.mark.django_db
def test_user_logout(client):
    user = User.objects.create_user(username="testuser", password="password123")
    client.login(username="testuser", password="password123")
    response = client.get(reverse("account:logout"))
    assert response.status_code == 302
    assert response.url == reverse("account:login")
