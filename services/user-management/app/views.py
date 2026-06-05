import secrets
from rest_framework import viewsets, status, views
from rest_framework.response import Response
from .models import User, Token
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegisterView(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate token
            token_str = secrets.token_hex(32)
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user, token=token_str)
            
            return Response({
                'token': token.token,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(email=email)
                if user.check_password(password) and user.is_active:
                    # Generate token
                    token_str = secrets.token_hex(32)
                    Token.objects.filter(user=user).delete()
                    token = Token.objects.create(user=user, token=token_str)
                    
                    return Response({
                        'token': token.token,
                        'user': UserSerializer(user).data
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({'error': 'Invalid credentials or user inactive'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
