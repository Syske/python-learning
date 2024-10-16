import json

json_obj = {"name": "John", "age": 30, "city": "New York"}
print("Before:", json_obj)

key_to_delete = "age"
if key_to_delete in json_obj:
    del json_obj[key_to_delete]

print("After:", json_obj)
