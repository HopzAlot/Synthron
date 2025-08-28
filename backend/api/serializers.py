from rest_framework import serializers
from .models import RequestBuild
class RequestBuildSerializer(serializers.ModelSerializer):
    class Meta:
        model= RequestBuild
        fields='__all__'