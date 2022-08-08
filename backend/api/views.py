from urllib import response

from django.http import HttpResponse
from products.serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['POST', 'GET'])
def api_home(request):
    #demo_data = {"title":"api_view"}
    serializer = ProductSerializer(data=request.data) 
    if serializer.is_valid(raise_exception=True): #Send the same as below response if invalid
        #instance = serializer.save()
        print(serializer.data)
        #return HttpResponse(instance)
        return Response(serializer.data) # Or ProductSerializer(instance).data

    return response({"invalid":"This field is required"}, status = 400)
