from django.db import models
# Create your models here.

class BuildRequest(models.Model):
    use_case= models.CharField(max_length=100)
    budget= models.FloatField()
    region= models.CharField(max_length=100)
    preferences= models.JSONField()
    created_at= models.DateField(auto_now_add=True)
