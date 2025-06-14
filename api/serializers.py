from rest_framework import serializers
from .models import BuildRequest
class BuildRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model= BuildRequest
        fields='__all__'