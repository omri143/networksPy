import helpers

JSON_ATTRIBUTES = ["id", "text", "answers", "correct_answer"]
dic = helpers.parse_json_doc("C:\\Users\\OMRI\\PycharmProjects\\networksPy\\chatlib\\questions.json")
"""
    print Json File
"""
x = {}
for i in range(0, len(dic["questions"])):
    x[str(dic["questions"][i][JSON_ATTRIBUTES[0]]).zfill(4)] = {"question": dic["questions"][i][JSON_ATTRIBUTES[1]],
                                                                "answers": dic["questions"][i][JSON_ATTRIBUTES[2]],
                                                                "correct": dic["questions"][i][JSON_ATTRIBUTES[3]]
                                                                }
    for k in range(0, len(JSON_ATTRIBUTES)):
        if k == 0:
            print(JSON_ATTRIBUTES[k] + ":", "\t", str(dic["questions"][i][JSON_ATTRIBUTES[k]]).zfill(4))
        else:
            print(JSON_ATTRIBUTES[k] + ":", "\t", str(dic["questions"][i][JSON_ATTRIBUTES[k]]))
        if k == 2:
            for j in range(0, len(dic["questions"][i][JSON_ATTRIBUTES[k]])):
                print("Answer ", str(j + 1) + ":", dic["questions"][i][JSON_ATTRIBUTES[k]][j])
    print("\n")

print(x)
for k in range(1, len(x) + 1):
    lst = helpers.parse_json_dict_to_lst(x, str(k).zfill(4), ["question", "answers", "correct"])
    print(lst)

z = helpers.parse_json_doc("C:\\Users\\OMRI\\PycharmProjects\\networksPy\\chatlib\\users.json")
for k in range(1, len(z) + 1):
    lst = helpers.parse_json_dict_to_lst(z, "omri", ["password", "score", "asked_questions"])
    print(lst)
