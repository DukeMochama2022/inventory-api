from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")

        if password is None or username is None:
            return Response({"error":"Please provide both username and password"},status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error":"The username is already taken"},status=status.HTTP_400_BAD_REQUEST)

        user=User.objects.create_user(username=username,password=password)
        token=Token.objects.create(user=user)
        return Response({"message":"User Created Successifully.","token":token.key},status=status.HTTP_201_CREATED)    

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            request.user.auth_token.delete()
            return Response({"message":"Logged out successfully."},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"Something went wrong during logout"}, status=status.HTTP_400_BAD_REQUEST)