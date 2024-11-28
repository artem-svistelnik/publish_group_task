from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class File(models.Model):
    upload_by = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(null=True, blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    error = models.CharField(null=True, blank=True, max_length=500)

    def __str__(self):
        return f"id: {self.id}; upload by: {self.upload_by.username}"


class DataRow(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    advertiser = models.CharField(max_length=500)
    brand = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField()
    format = models.CharField(max_length=500)
    platform = models.CharField(max_length=500)
    impr = models.PositiveIntegerField()

    def __str__(self):
        return (
            f"file id: {self.file.id}; row id: {self.id}; advertiser: {self.advertiser}"
        )
