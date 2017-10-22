from django.http import HttpResponse, JsonResponse
from .scrabble_ai import test
import json
import zmq

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

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://127.0.0.1:9001')

def scrabble_ai_v1(request):
    if request.method == "GET":
        board = request.GET.get("board") or "no"
        rack = request.GET.get("rack") or "df"

        socket.send_json({"board": board, "rack": rack})
        msg = socket.recv()
        msg = msg.decode("utf-8")
        msg = json.loads(msg)

        if msg["success"]:
            return success_response(msg["data"])
        else:
            return error_response(msg["error"])
    else:
        return error_response("Not a GET request")