from django.http import HttpResponse, JsonResponse
from .scrabble_ai import test
import json

###################
# Response types
###################
def success_response(data):
    return JsonResponse({"success": True, "data": data})

def error_response(error_message):
    return JsonResponse({"success": False, "error": error_message})

###################
# Django Views
###################

def hello_world(request):
    return success_response("Hello World!")

def scrabble_ai_v1(request):
    return success_response(test())
