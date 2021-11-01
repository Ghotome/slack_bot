import datetime
import json

import requests
import timeago

SLACK_BOT_TOKEN = "xoxb-2562066240742-2642882069457-4KXpdHOW1PyKxixMwLwMlB5U"
SLACK_APP_TOKEN = "xapp-1-A02JJ8F7VUK-2661098883766-d9644c915169a9ddfd3d5035db29a34075bd7cb6e7ba8272536f9a959a5dda13"
SLACK_SIGNING_SECRET = "76353595b80820112599ebfb461d9c95"
ZABBIX_URL = "https://zbbx.dianet.online/"
ZABBIX_API_URL = "https://zbbx.dianet.online/api_jsonrpc.php"
USERNAME = "apiuser"
PASSWORD = "FKbiAVg86G5FqViahwSkAbMk87ArJ6oMc"

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
    'speedtests': "https://graf.dianet.online/render/d-solo/qqAdGUv7z/home-page?orgId=1&var-brass={}&from=now&to=now-24h&panelId=20&width=1000&height=500&tz=Europe%2FZaporozhye"
}
slack_home_tab = json.dumps(
    {
        "type": "home",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Панель с основным функционалом бота*\n*Должен в личку отправлять запрошенные данные*"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Триггеры",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": "click_me_123",
                        "action_id": "triggers"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Аплинки",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": "click_me_123",
                        "action_id": "uplinks"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Пропущенные",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": "click_me_123",
                        "action_id": "missed_calls"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Speedtests BRAS",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": "click_me_123",
                        "action_id": "speedtests"
                    }
                ]
            },
            {
                "dispatch_action": True,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "login_handler"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Получть информацию об абоненте по логину\nВведите логин(CЕЙЧАС НЕ РАБОТАЕТ, НУЖЕН ДОСТУП В АБИЛС)",
                    "emoji": True
                }
            }
        ]
    }
)

speedtests_bras_select_modal = json.dumps(
    {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "DiaNet"
        },
        "submit": {
            "type": "plain_text",
            "text": "Готово"
        },
        "close": {
            "type": "plain_text",
            "text": "Отмена"
        },
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select an item"
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "BRAS43_Stella"
                            },
                            "value": "bras-stella"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "BRAS2_Liza1"
                            },
                            "value": "bras-liza"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Bras9_Yana"
                            },
                            "value": "bras-yana"
                        }
                    ],
                    "action_id": "select_bras_speedtest"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Выберите BRAS"
                }
            }
        ]
    }
)


def render_triggers_page(body):
    slack_home_tabb_triggers = json.dumps(
        {
            "type": "home",
            "callback_id": "home_view",
            "blocks": [
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{body}"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "На главную",
                                "emoji": True
                            },
                            "value": "click_me_123",
                            "action_id": "home_page"
                        }
                    ]
                }
            ]
        }
    )
    return slack_home_tabb_triggers


def get_user_info(login: str):
    # returns a dict which is contain
    # user information from abills and easypon

    url_user_info = (
        f'https://abill.dianet.online:9443/admin/index.cgi?qindex=7&search=1&type=10&header=1&json=1&LOGIN={login}'
        f'&EXPORT_CONTENT=USERS_LIST&SKIP_FULL_INFO=1&API_KEY=sdfgljkshdfghjdf2345js')
    try:
        response = json.loads(requests.get(url_user_info).content.decode('utf-8'))['DATA_1'][-1]
        address_name = str(response['address_full']).split(',')[0]
        address_number = str(response['address_full']).split(',')[1]

        user_info = {
            'fio': f"{response['fio']}",
            'subscriber_status': f'{response["login_status"]}',
            'address': f'{address_name[:1]}{address_name[1:].replace(address_name[1:], "*" * len(address_name[1:]))}, '
                       f'{address_number}',
            'tariff': '',
            'status': '',
            'cid': '',
            'onu_status': '',
            'onu_attenuation': '',
            'onu_position': ''
        }
    except KeyError:
        return 'Пользователь не найден'
    except IndexError:
        return 'Пользователь не найден'
    cid_url = (f"https://abill.dianet.online:9443/admin/index.cgi?UID={response['uid']}"
               f"&json=1&get_index=internet_user&header=1&API_KEY=sdfgljkshdfghjdf2345js")
    try:
        cid = json.loads(requests.get(cid_url).content.decode('utf-8'))
        user_info['status'] = cid['TABLE_INTERNET_ONLINE']['CAPTION'].split(' ')[0]
        user_info['tariff'] = cid['internet_user']['TP_NAME']
        user_info['cid'] = cid['internet_user']['CID']

    except KeyError:
        user_info['status'] = "Не удалось обнаружить активную услугу"
        user_info['tariff'] = "Не удалось обнаружить активную услугу"
        user_info['cid'] = "Не удалось обнаружить активную услугу"

    try:

        easypon_url_onu_id = (f'https://easypon.dianet.online/api/mac/fields?mac='
                              f'{user_info["cid"].replace(":", "").upper()}&key=eee4007ec41fbe778967ad59')
        ep_response = json.loads(requests.get(easypon_url_onu_id).content)['data'][-1]['onu_id']
        easypon_url_onu_info = (f"https://easypon.dianet.online//api/info_onu_id/fields?onu_id="
                                f"{ep_response}&key=eee4007ec41fbe778967ad59")
        onu_info = json.loads(requests.get(easypon_url_onu_info).content.decode('utf-8'))['data']

        user_info['onu_status'] = str(onu_info['state']) \
            .replace('3', ':white_check_mark:Online') \
            .replace('1', ':x:LOS') \
            .replace('2', ':exclamation:Synchronized') \
            .replace('4', ':warning:Power Off') \
            .replace('6', ':exclamation:Offline') \
            .replace('7', ':x:LOS')
        user_info['onu_position'] = f"{str(onu_info['olt_name'])}, {str(onu_info['position_onu'])}"
        user_info['onu_attenuation'] = (f"{str(float('{0:.2f}'.format(onu_info['measure_onu'])))}/"
                                        f"{str(float('{0:.2f}'.format(onu_info['measure_olt'])))}")
        return user_info

    except KeyError:
        user_info['onu_status'] = 'ОНУ не найдена'
        user_info['onu_position'] = 'ОНУ не найдена'
        user_info['onu_attenuation'] = 'ОНУ не найдена'
        return user_info

    except TypeError:
        user_info['onu_status'] = 'ОНУ не найдена'
        user_info['onu_position'] = 'ОНУ не найдена'
        user_info['onu_attenuation'] = 'ОНУ не найдена'
        return user_info


def get_list_of_triggers(auth):
    all_triggers_request = requests.post(ZABBIX_API_URL,
                                         json={
                                             "jsonrpc": "2.0",
                                             "method": "trigger.get",
                                             "params": {
                                                 "output": [
                                                     "host",
                                                     "description",
                                                     "priority"
                                                 ],
                                                 "expandDescription": "True",
                                                 "active": "True",
                                                 "monitored": "True",
                                                 "min_severity": 3,
                                                 "filter": {
                                                     "value": "1",
                                                     "status": "0"
                                                 }

                                             },
                                             "id": 3,
                                             "auth": auth
                                         })

    timestamps_request_all = requests.post(ZABBIX_API_URL,
                                           json={
                                               "jsonrpc": "2.0",
                                               "method": "event.get",
                                               "params": {
                                                   "output": [
                                                       "name",
                                                       "clock",
                                                       "objectid",
                                                       "acknowledged",
                                                   ],
                                                   "select_acknowledges": [
                                                       "message"
                                                   ],
                                                   "filter": {
                                                       "value": "1"
                                                   },
                                                   "selectTags": "extend",
                                                   "searchByAny": "false",
                                                   "sortfield": [

                                                       "eventid",
                                                       "clock"
                                                   ],
                                                   "sortorder": "DESC"
                                               },
                                               "id": 4,
                                               "auth": auth
                                           })
    triggers = json.loads(all_triggers_request.content)['result']
    ack_events = json.loads(timestamps_request_all.content)['result']
    result = ''

    if not triggers:
        result = 'На текущий момент, список проблем пуст.'
    else:
        for trigger in triggers:
            max_age = ""
            for ack_event in ack_events:
                if ack_event['name'] != trigger['description']:
                    continue
                elif ack_event['clock'] > max_age:
                    max_age = ack_event['clock']
                    timestamp = (timeago.format(datetime.datetime.now(), int(max_age), 'ru'))
                    if ack_event['acknowledged'] != '0':
                        if len(ack_event['acknowledges']) >= 1 and ack_event['acknowledges'][-1]['message']:
                            ack_message = str(ack_event['acknowledges'][-1]['message'])
                            ack_link = (f"{ZABBIX_URL}"
                                        f"zabbix.php?action=popup&popup_action=acknowledge.edit&eventids[0]="
                                        f"{str(ack_event['eventid'])}")
                            message_line = f"<{ack_link}|:white_check_mark:>*Проблема: {trigger['description']}*"
                            time = f"\n*Создана:* {timestamp} назад"
                            result += f"{message_line}\n*Комментарий:* " \
                                      f"{ack_message}\r{time.replace('завтра', '1 день').replace('через', '')}\n\n"
                        else:
                            ack_link = (f"{ZABBIX_URL}"
                                        f"zabbix.php?action=popup&popup_action=acknowledge.edit&eventids[0]="
                                        f"{str(ack_event['eventid'])}")
                            message_line = f"<{ack_link}|:white_check_mark:>*Проблема: {trigger['description']}*"
                            time = f"\n*Создана:* {timestamp} назад"
                            result += f"{message_line}\r{time.replace('завтра', '1 день').replace('через', '')}\n\n"

                    else:
                        ack_link = (f"{ZABBIX_URL}"
                                    f"zabbix.php?action=popup&popup_action=acknowledge.edit&eventids[0]="
                                    f"{str(ack_event['eventid'])}")
                        message_line = f"<{ack_link}|:x:>*Проблема: {trigger['description']}*"
                        time = f"\n*Создана:* {timestamp} назад"
                        result += f"{message_line}\r{time.replace('завтра', '1 день').replace('через', '')}\n\n"
    return result
