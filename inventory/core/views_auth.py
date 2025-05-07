from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "User registered successfully.",
                "token": token.key,
                "role": user.profile.role
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            request.user.auth_token.delete()
            return Response({"message":"Logged out successfully."},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":"Something went wrong during logout"}, status=status.HTTP_400_BAD_REQUEST)