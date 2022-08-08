from rest_framework import serializers

from products.models import Product
from django.contrib.auth.models import User

class UserProductInlineSerializer(serializers.Serializer): # Just serializes, doesn't care about fields
    title = serializers.CharField()
    url = serializers.HyperlinkedIdentityField(
        view_name="product-detail",
        lookup_field = "title",
        read_only = True
    )


class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField()
    id = serializers.IntegerField(read_only = True) 
    # hell = serializers.IntegerField() --> does not match any attribute or key on the `User` instance.
    other_products = serializers.SerializerMethodField(read_only=True) # Method should be defined

    def get_other_products(self, obj):
        print(self.context)
        user = obj
        qs = user.product_set.all() # Reverse relationship
        # for object in qs:
        #     print(object.title)
        # qs = User.objects.all() # Results in error --> User object has no title attribute
        return UserProductInlineSerializer(qs, many=True, context=self.context).data


