from django.db import models

# FOR NOW: SUBMISSION IS IMMUTABLE FOR THE USER
class Submission(models.Model):
    answers = models.JSONField()
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
