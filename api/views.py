from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import BuildRequest
from .serializers import BuildRequestSerializer
import requests
from .agents.central_agent import CentralAgent
from .agents.llama import generate_llama_response
# Create your views here.

@api_view(['GET'])
def getdata(request):
    data=BuildRequest.objects.all()
    serializer= BuildRequestSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def configure_build(request):
    prompt = request.data.get("prompt")
    if not prompt:
        return Response({"error": "Prompt is required"}, status=400)

    manager = CentralAgent(prompt)
    build_response = manager.run()
    return Response(build_response, status=status.HTTP_200_OK)

@api_view(['POST'])
def llama_generate(request):
    prompt = request.data.get("prompt")
    if not prompt:
        return Response({"error": "Prompt is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        result = generate_llama_response(prompt)
        return Response({"response": result}, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({"error": f"Request failed: {str(e)}"}, status=status.HTTP_502_BAD_GATEWAY)
    except ValueError as ve:
        return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def llama_ui(request):
    return render(request, 'index.html')
