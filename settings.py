SLACK_BOT_TOKEN = "xoxb-2562066240742-2642882069457-4KXpdHOW1PyKxixMwLwMlB5U"
SLACK_APP_TOKEN = "xapp-1-A02JJ8F7VUK-2661098883766-d9644c915169a9ddfd3d5035db29a34075bd7cb6e7ba8272536f9a959a5dda13"
SLACK_SIGNING_SECRET = "76353595b80820112599ebfb461d9c95"
ZABBIX_URL = "https://zbbx.dianet.online/"
ZABBIX_API_URL = "https://zbbx.dianet.online/api_jsonrpc.php"
USERNAME = "apiuser"
PASSWORD = "bA5r5zT9g9cwbcT4UxXpYw2G"
DEBUG = True
log_file = '/home/fishhead/Desktop/slack_bot_logging.txt'

api_tokens = {
    "abills_settings": {
        'abon_link': 'https://abill.dianet.online:9443/admin/index.cgi?index=15&UID=',
        'token': 'sdfgljkshdfghjdf2345js'
    },
    "easypon_settings": {
        'token': 'eee4007ec41fbe778967ad59',
        'link': 'https://easypon.dianet.online/'
    },
    'grafana': {
        'auth': {'Authorization': 'Bearer eyJrIjoieTdCU2ViZWFwaHIwNkVRbVhrQU91a2FXZ3MxNW1wVjUiLCJuIjoiQVBJIiwiaWQiOjF9'}
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
    "U02J2SEMQ86": {"name": "Оксов Станислав", "userside_id": "190"},
    "U02J9JR3XQB": {"name": "Хилобок Ксения", "userside_id": "94"},
    "U02J2SEKBFY": {"name": "Стародуб Кристина", "userside_id": "126"},
    "U02JN6VRE0H": {"name": "Коломиец Павел", "userside_id": "191"},
    "U02J9JR03AP": {"name": "Чиглашвили Кирилл", "userside_id": "193"},
    "U02J9JRG87M": {"name": "Хорошайлова Оксана", "userside_id": "143"},
    "U02J9JR9CAF": {"name": "Полякова Мария", "userside_id": "156"},
    "U02J9HQSBJ7": {"name": "Лупынина Анастасия", "userside_id": "158"},
    "U02J2SEPZ2A": {"name": "Петручук Любовь", "userside_id": "163"},
    "U02J9JR7RFV": {"name": "Нефёдов Егор", "userside_id": "168"},
    "U02J2SERRC6": {"name": "Зрожевский Анатолий", "userside_id": "170"},
    "U02J9JR1V0T": {"name": "Жирова Полина", "userside_id": "189"},
    "U02J9JR5VFV": {"name": "Лысенко Мария", "userside_id": "197"},
    "U02JLTM0GN5": {"name": "Стажер", "userside_id": "40"},
    "U02J6JY6GP7": {"name": "Хренкина Наталия", "userside_id": "192"},
    "U02J9JRES9H": {"name": "Арсланов Артем", "userside_id": "204"},
    "U02J9JRJ79R": {"name": "Константин Гуреев", "userside_id": "201"},
    "U02J9JRB2SF": {"name": "Березовский Вадим", "userside_id": "206"},
    "U02J6GS8HQV": {"name": "Кристина Костенко", "userside_id": "199"},
    "U02J6GRLASH": {"name": "Елена Красно", "userside_id": "205"},
    "U02J9JRD2JX": {"name": "Максим Сырбу", "userside_id": "208"},
    "U02JTSMT2BF": {"name": "Сергей Яремченко", "userside_id": "211"},
    "U02JMSFPMV3": {"name": "Евгения Цыха", "userside_id": "210"},
    "U02JA2E9YFP": {"name": "Алексей Кирносенко"},
    "U02JRKSQ53K": {"name": "Александр Стародуб"},
    "U02JRKSNEQZ": {"name": "Евгений Гаркуша"},
    "U02JRKSRQ8H": {"name": "Шагов Егор"},
    "U02JA2E2HB7": {"name": "Шалык Павел"},
    "U02JA2E3CER": {"name": "Шевченко Денис"},
    "U02JA2DSNQM": {"name": "Сергей Бондаренко"},
    "U02JA2E8F45": {"name": "Шевченко Илья"},
    "U02JH6M31R7": {"name": "Зайцев Александр"},
    "U02J1AG6AJZ": {"name": "Александр Балюшко"},
    "U02HV0KFB1A": {"name": "Дмитренко Дмитрий"},
    "U02JU897ML0": {"name": "Смык Евгений"}

}
