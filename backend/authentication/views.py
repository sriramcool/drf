from ast import Return
from django.shortcuts import redirect
from requests import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view


# Create your views here.

@api_view(["POST", "GET"])
def login(request):
    user = request.user
    if request.method == "GET":
        return Response()

    if user.is_authenticated:
        return Response({"detail":"already authenticated"})

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(username=username, password=password)
    if user is not None:
        login(user, request)
        return redirect("viewcreate") 

    return Response({"detail":"invalid credentials"})

    
