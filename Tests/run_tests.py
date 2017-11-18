import urllib.request
import json
import operator


tests_file = open("tests.txt", "r")
answers_file = open("answers.txt", "r")

count = 1

for test_case_link, answer_dict in zip(tests_file, answers_file):
    response = urllib.request.urlopen(test_case_link).read().decode('utf-8')
    response_list = sorted(json.loads(response).items(), key=operator.itemgetter(0))

    answer_list = sorted(json.loads(answer_dict).items(), key=operator.itemgetter(0))

    if response_list == answer_list:
        print("Test " + str(count) + "\t\t" + " \033[92mPASSED\033[0m")
    else:
        print("Test " + str(count) + "\t\t" + " \033[91mFAILED\033[0m")

    count += 1

tests_file.close()
answers_file.close()
