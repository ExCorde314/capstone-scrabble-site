from django.http import HttpResponse, JsonResponse
from .scrabble_ai import test
import json
import zmq

###################
# Response types
###################
def robot_response(new_word, N, param1, param2, param3, score):
    return JsonResponse({"success": True, "word": new_word, \
"N": N, "param1": param1, "param2": param2, "param3": param3, "score": score})

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

            pickup_locations = []
            dropoff_locations_X = []
            dropoff_locations_Y = []

            move_information = msg["data"]
            last_space = len(move_information) - move_information.rfind(' ')

            score = int(move_information[-last_space + 1:])

            space_index = 0
            for character in move_information:
                if character == ' ':
                    break
                space_index += 1

            new_word = move_information[0:space_index]

            row = int(move_information[space_index+2])
            move_information = move_information[space_index:]

            for character in move_information:
                if character == ' ':
                    break
                space_index += 1

            row_index = (move_information.split(",")[0]).split("(")[1]
            col_index = move_information.split(",")[1]
            row = int(row_index)
            col = int(col_index)
            direction = move_information.split(",")[2][0]

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
                board_index = ((row*15) + col)

                if board[board_index] == required_character:

                    if direction == "H":
                        col += 1
                    else:
                        row += 1
                    continue

                try:
                    pickup_location = rack_dictionary[required_character][0]
                    # Once selected for a pick up - remove that location from the dict
                    del rack_dictionary[required_character][0]
                except:
                    # THIS SHOULD NEVER HAPPEN
                    # MEANS THAT THE REQUIRED WORD IS NOT IN THE RACK
                    return error_response("could not find the letter in the rack")


                dropoff_location = (row, col)

                # robot_movements.append((pickup_location, dropoff_location[0], dropoff_location[1]))
                pickup_locations.append(pickup_location)
                dropoff_locations_X.append(dropoff_location[0])
                dropoff_locations_Y.append(dropoff_location[1])

                if direction == "H":
                    col += 1
                else:
                    row += 1

            # format pickup_locations, dropoff_locations_X, dropoff_locations_Y
            N = len(pickup_locations)

            if N == 0:
                return error_response("no moves to make found")

            param1 = ','.join(str(e) for e in pickup_locations)
            param2 = ','.join(str(e) for e in dropoff_locations_X)
            param3 = ','.join(str(e) for e in dropoff_locations_Y)

            return robot_response(new_word, N, param1, param2, param3, score)

        else:
            return error_response(msg["error"])
    else:
        return error_response("Not a GET request")
