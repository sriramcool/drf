from rest_framework import generics, authentication, permissions

from .mixins import UserQuerysetMixin
from .serializers import ProductSerializer
from .models import Product

from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .permissions import IsOwnerOrReadOnly 

class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer 

    def perform_create(self, serializer): # Naming --> "perform_create"
        title = serializer.validated_data.get("title") # Validated_data is validated according to the settings in serializers
        description = serializer.validated_data.get("description") or None

        if description is None:
            description = title

        serializer.save(description = description) # updates

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all() # Searches from this queryset
    serializer_class = ProductSerializer 
    lookup_field = "title"

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all().order_by("?") # Queryset --> attribute that will be serializised 
    serializer_class = ProductSerializer 

class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer 
    #permission_classes = [IsOwnerOrReadOnly]
    #lookup_field = "pk"
 
    def perform_update(self, serializer): # Overrides default update
        instance = serializer.save()
        print(serializer.data)

class ProductDeleteAPIView(generics.DestroyAPIView):
    pass

class ProductListCreateApiView(UserQuerysetMixin, generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #authentication_classes = [authentication.SessionAuthentication]
 
    def perform_create(self, serializer):
        title = serializer.validated_data.get("title")
        description = serializer.validated_data.get("description")

        if description is None:
            description = title

        serializer.save(description = description)
        print(serializer.data)

    # def get_queryset(self): # Get custom query set (Use this to display post in user's profile)
    #     qs = super().get_queryset()
    #     request = self.request
    #     user = request.user
    #     return qs.filter(user= request.user)

@api_view(['GET', 'POST'])
def api(request, pk=None, *args, **kwargs):
    method = request.method

    if method == 'GET':
        if pk is not None:
            # Detailedview
            queryset = get_object_or_404(Product, pk=pk) # Rest framework hanles the 404 response as json
            print(queryset)
            data = ProductSerializer(queryset, context={'request':request}).data # context is required to create absolute url in the UserProductInlineSerializer and in ProductSerializer
            print(data)
            return Response(data=data)

        else:
            # Listview
            queryset = Product.objects.all()
            data = ProductSerializer(queryset, many=True).data
            return Response(data)
        

    if method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            #instance = serializer.save()
            title = serializer.validated_data.get("title")
            description = serializer.validated_data.get("description") or None
            if description is None:
                description = title

            serializer.save(description = description)                  
        return Response(serializer.data) # Takes dictionary
