from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    owner = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    schema = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField(null=True)
