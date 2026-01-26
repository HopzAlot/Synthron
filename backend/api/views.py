from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RequestBuild
from .serializers import RequestBuildSerializer
from .agents.central_agent import CentralAgent  
from .agents.llama import generate_llama_response 
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

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
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=401)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=200)

class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=400)

        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                "access": str(refresh.access_token)
            })
        except Exception:
            return Response({"error": "Invalid refresh token"}, status=401)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"message": "Logged out"})

class GetDataView(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        data = RequestBuild.objects.all()
        serializer = RequestBuildSerializer(data, many=True)
        return Response(serializer.data)



@method_decorator(csrf_exempt, name="dispatch")
class ConfigureBuildView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        print("USER:", request.user)
        print("AUTH:", request.auth)
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
            result = generate_llama_response(prompt)
            return Response({"response": result}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def llama_ui(request):
    return render(request, 'index.html')