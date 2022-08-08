from .models import Product
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

def badwords_validator(value):
    if "fuck" in value:
        raise serializers.ValidationError("No badwords allowed")

    return value

unique_title = UniqueValidator(Product.objects.all(), lookup="iexact")
