from DiscordHooks import Hook
import os

URL = os.environ.get('WEBHOOK')

def sendData(embeds):
    hook = Hook(hook_url=URL,embeds=embeds,content='@everyone')
    try:
        hook.execute()
        return True
    except:
        return False