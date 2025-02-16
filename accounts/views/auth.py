from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from ..serializers.auth import LoginSerializer
from ..models import UserToken
from django.contrib.auth import authenticate


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['password']
            phone=serializer.validated_data['phone']
            device_id=serializer.validated_data['device_id']
            
            user = authenticate(phone=phone, password=password)
            
            if user:
                if not user.is_active:
                    return Response(
                        {"error": "تم تعطيل الحساب تواصل معنا لحل المشكلة"},
                        status=status.HTTP_403_FORBIDDEN,
                    )
                    # Check if the user already has an active session
                if UserToken.objects.filter(user=user).exists():
                    userToken=UserToken.objects.get(user=user)
                    if userToken.device_id != device_id:
                        return Response(
                            {"error": "تم تسجيل الدخول من جهاز أخر يرجى التواصل معنا للحصول على حساب جديد"},
                            status=status.HTTP_403_FORBIDDEN,
                        )
                else:
                    UserToken.objects.create(user=user, device_id=device_id)
                    

                # Generate new tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Store the new token
            

                return Response({
                    'refresh': str(refresh),
                    'access': access_token,
                }, status=status.HTTP_200_OK)         
            else:
                
                return Response(
                        {"error": "الرقم أو كلمة المرور خطأ,يرجى المحاولة مرة أخرى"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    def post(self, request):
        token = request.data.get('token')
        if token:
            try:
                # Decode the token to get the user
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                # Delete the token from the UserToken model
                UserToken.objects.filter(user_id=user_id).delete()
                return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)