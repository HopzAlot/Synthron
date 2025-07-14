from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RequestBuild
from .serializers import RequestBuildSerializer
from .agents.central_agent import CentralAgent  # should be sync version
from .agents.llama import generate_llama_response  # should be sync version
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    permission_classes=[AllowAny]

    def post(self, request):
        username= request.data.get('username')
        password=request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and Password required!!'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_409_CONFLICT)
        
        user=User.objects.create_user(username=username, password=password)
        return Response({'message': 'User created Successfully'}, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        user=authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'}, status=401)
        
        refresh=RefreshToken.for_user(user)
        response=Response({'message': 'Login Successful'})
        
        #Setting JWT tokkens in HTTPOnly Cokkies:

        response.set_cookie('access', str(refresh.access_token), httponly=True, secure=True, samesite='Lax', max_age=300)
        response.set_cookie('refresh',str(refresh), httponly=True, secure=True, samesite='Lax', max_age=604800)
        return response
class RefreshTokenView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        refresh_token=request.COOKIES.get('refresh')
        if refresh_token is None:
              return Response({'error': 'No refresh token found in cookies'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh=RefreshToken(refresh_token)
            response = Response({'message': 'Token refreshed successfully'})
            response.set_cookie(
                'access',
                str(refresh.access_token),
                httponly=True,
                secure=True,
                samesite='Lax',
                max_age=300
            )
            return response

        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh')
        response = Response({'message': 'Logged out successfully'})

        if refresh_token is not None:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
            except Exception:
                # Token may be invalid or already blacklisted, ignore errors
                pass

        # Delete the JWT cookies
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
    
# class GetDataView(APIView):
#     permission_classes=[IsAuthenticated]
#     def get(self, request):
#         data = BuildRequest.objects.all()
#         serializer = BuildRequestSerializer(data, many=True)
#         return Response(serializer.data)


class ConfigureBuildView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            manager = CentralAgent(prompt)
            build_response = manager.run()

            #saving the build to history
            RequestBuild.objects.create(
                user=request.user,
                prompt=prompt,
                summary=build_response.get('summary'),
                build=build_response.get('build'),
                total=build_response.get('total'),
                issues=build_response.get('issues')
            )
            return Response(build_response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BuildHistory(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        history=RequestBuild.objects.filter(user=request.user).order_by('-created_at')
        serializer=RequestBuildSerializer(history, many=True)
        return Response(serializer.data)
class LlamaGenerateView(APIView):
    def post(self, request):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response({"error": "Prompt is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            result = generate_llama_response(prompt)  # sync llama call
            return Response({"response": result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def llama_ui(request):
    return render(request, 'index.html')
