from django.db import models
from django.contrib.auth.models import User

class RequestBuild(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='builds')
    prompt=models.TextField(default="Unknown Prompt")
    summary=models.TextField(blank=True, null=True)
    build=models.JSONField(blank=True, null=True)
    total=models.FloatField(blank=True, null=True)
    issues=models.JSONField(blank=True, null=True)
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Build by {self.user.username} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"