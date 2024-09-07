from rest_framework import serializers
from .models import File, CustomUser, Page


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "password", "is_superuser")
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data["email"],
        )
        user.set_password(validated_data["password"])  # Хеширование пароля
        user.save()
        return user


class FileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    _destroy = serializers.BooleanField(
        required=False, default=False
    )  # Дополнительное поле для удаления

    class Meta:
        model = File
        fields = ["id", "_destroy"]


class FileReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            "id",
            "name",
            "file",
            "uploaded_at",
        ]


class PageSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, required=False)

    class Meta:
        model = Page
        fields = ["id", "title", "content", "slug", "files"]

    def update(self, instance, validated_data):
        files_data = validated_data.pop("files", [])
        instance = super().update(instance, validated_data)

        for file_data in files_data:
            if file_data.get("_destroy", False):
                instance.files.remove(file_data["id"])
            else:
                instance.files.add(file_data["id"])

        return instance


class PageReadSerializer(serializers.ModelSerializer):
    files = FileReadSerializer(
        many=True, read_only=True
    )  # Вложенный сериализатор для чтения данных

    class Meta:
        model = Page
        fields = ["id", "title", "content", "slug", "files"]
