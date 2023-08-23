SLACK_BOT_TOKEN = ""
SLACK_APP_TOKEN = ""
SLACK_SIGNING_SECRET = ""
ZABBIX_URL = "https://zbbx.dianet.online/"
ZABBIX_API_URL = "https://zbbx.dianet.online/api_jsonrpc.php"
USERNAME = ""
PASSWORD = ""
DEBUG = True
log_file = '/var/log/slack_bot/slack_bot_logging.txt'

api_tokens = {
    "abills_settings": {
        'abon_link': 'admin/index.cgi?index=15&UID=',
        'token': 'sdfgljkshdfghjdf2345js'
    },
    "easypon_settings": {
        'token': 'eee4007ec41fbe778967ad59',
        'link': 'https://easypon.dianet.online/'
    },
    'grafana': {
        'auth': {'Authorization': 'Bearer'}
    }
}

images_links = {
    'uplinks': "https://graf.dianet.online/render/d-solo/qqAdGUv7z/home-page?orgId=1&from=now&to=now-24h&panelId=2&width=1100&height=400&tz=Europe%2FZaporozhye",
    'fuel': "https://graf.dianet.online/render/d-solo/Sarw7vlMk/fuel-level?orgId=1&from=now&to=now-24h&panelId=2&width=1000&height=500&tz=Europe%2FZaporozhye",
    'speedtests': "https://graf.dianet.online/render/d-solo/qqAdGUv7z/home-page?orgId=1&var-brass={}&from=now&to=now-24h&panelId=20&width=1000&height=500&tz=Europe%2FZaporozhye",
    'missed_calls': 'https://graf.dianet.online/render/d-solo/cHENmG8Mk/asterisk?orgId=1&from=now&to=now&panelId=2&width=800&height=1000&tz=Europe%2FZaporozhye',
    'temp': 'https://graf.dianet.online/render/d-solo/0kaml5jWz/temp?orgId=1&refresh=10s&from=now&to=now-24h&panelId=2&width=1000&height=500&tz=Europe%2FZaporozhye',
    'calls_statistics': "https://graf.dianet.online/render/d-solo/cHENmG8Mk/asterisk?orgId=1&from=now&to=now-24h&panelId=4&width=1000&height=500&tz=Europe%2FZaporozhye",
    'callback_statistics': 'https://graf.dianet.online/render/d-solo/cHENmG8Mk/asterisk?orgId=1&from=now&to=now-24h&panelId=6&width=1000&height=500&tz=Europe%2FZaporozhye'
}

operators = {

    "U02J9JR7RFV": {"name": "Нефёдов Егор", "userside_id": "168"}


}
