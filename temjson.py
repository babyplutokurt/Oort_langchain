import json

# Data to be written
dictionary = {"employees":[
    {"name":"Shyam", "email":"shyamjaiswal@gmail.com"},
    {"name":"Bob", "email":"bob32@gmail.com"},
    {"name":"Jai", "email":"jai87@gmail.com"}
]}

with open("Json_files/Account_balance.json", "w") as outfile:
    json.dump(dictionary, outfile)