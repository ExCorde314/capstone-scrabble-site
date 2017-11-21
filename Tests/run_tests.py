import urllib.request
import json
import operator
import time


tests_file = open("tests.txt", "r")
answers_file = open("answers.txt", "r")

count = 1

for test_case_link, answer_line in zip(tests_file, answers_file):
    passed = False
    response = urllib.request.urlopen(test_case_link).read().decode('utf-8')
    response_list = sorted(json.loads(response).items(), key=operator.itemgetter(0))

    answer_lists = answer_line.split('||')

    for answer_dict in answer_lists:
        answer_list = sorted(json.loads(answer_dict).items(), key=operator.itemgetter(0))
        if response_list == answer_list:
            print("Test " + str(count) + "\t\t" + " \033[92mPASSED\033[0m")
            passed = True
            break

    if passed == False:
        print("Test " + str(count) + "\t\t" + " \033[91mFAILED\033[0m")

    count += 1
    time.sleep(1) # wait in between tests 

tests_file.close()
answers_file.close()
