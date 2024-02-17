from json import loads

json_string = '''
            {"Age": 9}
              '''

json_dict = loads(json_string)
print(json_dict)
print(json_dict["Age"])
