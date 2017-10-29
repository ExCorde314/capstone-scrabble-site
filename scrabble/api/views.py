from django.http import HttpResponse, JsonResponse
from .scrabble_ai import test
import json
import zmq

###################
# Response types
###################
def robot_response(new_word, robot_movements):
    return JsonResponse({"success": True, "word": new_word, "actions": robot_movements})

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

            move_information = msg["data"]

            space_index = 0
            for character in move_information:
                if character == ' ':
                    break
                space_index += 1

            new_word = move_information[0:space_index]

            row = int(move_information[space_index+2]) - 1
            col = int(move_information[space_index+4]) - 1
            direction = move_information[space_index+6]

            rack_dictionary = {}
            rack_index = 0

            robot_movements = []

            for rack_character in rack:
                try:
                    rack_dictionary[rack_character].append(rack_index)
                except:
                    rack_dictionary[rack_character] = [rack_index]
                rack_index += 1

            for required_character in new_word:
                board_index = (row*15) + col
                
                if board[board_index] == required_character:
                    continue

                pickup_location = rack_dictionary[required_character][0]
                del rack_dictionary[required_character][0]

                dropoff_location = (row, col)

                robot_movements.append((pickup_location, dropoff_location[0], dropoff_location[1]))

                if direction == "H":
                    col += 1
                else:
                    row += 1



            return robot_response(new_word, str(robot_movements))
        else:
            return error_response(msg["error"])
    else:
        return error_response("Not a GET request")
