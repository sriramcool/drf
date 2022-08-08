from asyncore import read
from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer
from .models import Product

from .validators import badwords_validator, unique_title

class ProductSerializer(serializers.ModelSerializer): # model serializers requires meta 
    owner = UserPublicSerializer(source="user", read_only=True) # an explicit `.create()` method for serializer `products.serializers.ProductSerializer` is needed if it's not read only to save 
    my_discount = serializers.SerializerMethodField(read_only = True)
    url = serializers.SerializerMethodField(read_only= True)
    url2 = serializers.HyperlinkedIdentityField(view_name="product-detail", lookup_field = "title")
    title = serializers.CharField(validators=[badwords_validator, unique_title]) #  Custom field validation
    user_data = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'url',
            'url2',
            'title',
            'description',
            'price',
            'sale_price',
            'my_discount',
            'user_data',
            'owner',
        ]
        read_only_fields = ['url', 'user_data']

    def get_user_data(self, obj):
        if obj.user is None:
            return "NO user associated with the object"
        return {
            "name":obj.user.username,
            "pass":obj.user.password
        }

    # def validate_title(self, title):
    #     if "fuck" in title:
    #         raise serializers.ValidationError("Bad words not allowed")
        
    #     return title # Final validation 
    
    # def validate_price(self, value):
    #     return "hello" # Raises error


    def get_url(self, obj):
        #return f'api/products/{obj.title}/'
        request = self.context.get("request")
        return reverse("product-detail", kwargs={"title":obj.title}, request = request)

    def get_my_discount(self, obj):
        # obj -> instance.
        if not hasattr(obj, "id"):
            return None

        if not isinstance(obj, Product):
            return None

        return obj.get_discount() # if instance is passed
    
