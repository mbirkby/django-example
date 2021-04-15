from rest_framework import serializers
from rest_framework.response import Response
from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail"

        )
