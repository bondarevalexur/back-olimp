from rest_framework import serializers
from ..models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application  # Модель, с которой связан сериализатор
        fields = '__all__'
