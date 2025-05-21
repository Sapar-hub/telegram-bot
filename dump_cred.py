import json

with open('credentials.json') as f:
    creds = json.load(f)
with open('token.json') as t:
    tok = json.load(t)
#print(json.dumps(creds))
print(json.dumps(tok))