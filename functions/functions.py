import datetime
import json
import traceback

import requests
import timeago
from slack_sdk.errors import SlackApiError

import settings
import views.views


def get_user_info(login: str):
    """

    :param login:
    :return: returns DICT which contain data:
    DICT = {
            'fio': STRING, FULL NAME,
            'subscriber_status': STRING, CURRENT STATUS OF BILLING RECORD,
            'address': STRING, ADDRESS FORMATTED AS "ABCDEF, 10 => A*****, 10"
            'tariff': STRING, TARIFF NAME,
            'status': STRING, CURRENT STATUS OF INTERNET SESSION,
            'cid': STRING, CID PARAMETER,
            'onu_status': STRING, STATUS OF ONU,
            'onu_attenuation': STRING, FORMATTED AS "ONU/OLT",
            'onu_position': STRING, POSITION ONU, FORMATTED AS "OLT, POSITION"
    }
    """

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


def zabbix_event_acknowledge(auth, message, event_id):
    body = {
        "jsonrpc": "2.0",
        "method": "event.acknowledge",
        "params": {
            "eventids": f"{event_id}",
            "action": 6,
            "message": f"{message}"
        },
        "auth": auth,
        "id": 1
    }
    event_acknowledge = requests.post(settings.ZABBIX_API_URL, data=body)
    return event_acknowledge


def get_list_of_triggers(auth):
    """

    :param auth:
    :return: returns STRING which contains all triggers from zabbix, already formatted etc.
    """
    all_triggers_request = requests.post(settings.ZABBIX_API_URL,
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

    timestamps_request_all = requests.post(settings.ZABBIX_API_URL,
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
    block_message = views.views.empty_blocks
    problems = {}

    if not triggers:
        block_message = 'На текущий момент, список проблем пуст.'
        return block_message
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
                            ack_message = f"*Комментарий:* {str(ack_event['acknowledges'][-1]['message'])}"
                            ack_link = (f"{settings.ZABBIX_URL}"
                                        f"zabbix.php?action=popup&popup_action=acknowledge.edit&eventids[0]="
                                        f"{str(ack_event['eventid'])}")
                            message_line = f":white_check_mark:*Проблема: {trigger['description']}*"
                            time = f"\n*Создана:* {timestamp} назад".replace('завтра', '1 день').replace('через', '')
                            result = views.views.render_one_trigger_line(message_line, ack_link,
                                                                         f"{ack_message}\r{time}\n\n")
                            block_message['blocks'].append(result)
                            problems[message_line.replace(':white_check_mark:Проблема: ', '').replace('*', '')] = ack_link.split('=')[-1]
                        else:
                            ack_link = (f"{settings.ZABBIX_URL}"
                                        f"zabbix.php?action=popup&popup_action=acknowledge.edit&eventids[0]="
                                        f"{str(ack_event['eventid'])}")
                            message_line = f":white_check_mark:*Проблема: {trigger['description']}*"
                            time = f"\n*Создана:* {timestamp} назад".replace('завтра', '1 день').replace('через', '')
                            result = views.views.render_one_trigger_line(message_line, ack_link, f"{time}\n\n")
                            block_message['blocks'].append(result)
                            problems[message_line.replace(':white_check_mark:Проблема: ', '').replace('*', '')] = ack_link.split('=')[-1]
                    else:
                        ack_link = (f"{settings.ZABBIX_URL}"
                                    f"zabbix.php?action=popup&popup_action=acknowledge.edit&eventids[0]="
                                    f"{str(ack_event['eventid'])}")
                        message_line = f":x:*Проблема: {trigger['description']}*"
                        time = f"\n*Создана:* {timestamp} назад".replace('завтра', '1 день').replace('через', '')
                        result = views.views.render_one_trigger_line(message_line, ack_link, f"{time}\n\n")
                        block_message['blocks'].append(result)
                        problems[message_line.replace(':x:Проблема: ', '').replace('*', '')] = ack_link.split('=')[-1]
    return block_message, problems


def zabbix_login(url: str):
    """

    :param url:
    :return: AUTH TOKEN, STRING
    """
    login = requests.post(url,
                          json={
                              "jsonrpc": "2.0",
                              "method": "user.login",
                              "params": {
                                  "user": settings.USERNAME,
                                  "password": settings.PASSWORD},
                              "id": 1
                          })

    auth = login.json()['result']
    return auth

auth = zabbix_login(settings.ZABBIX_API_URL)
print(get_list_of_triggers(auth)[0])

def update_home_tab(tab, user_id, client, log):
    """

    :param tab:
    :param user_id:
    :param client:
    :param log:
    :return: NONE
    """
    try:
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            # the user that opened your app's app home
            user_id=user_id,
            # the view object that appears in the app home
            view=tab
        )

    except Exception as e:
        log.error(f"Error updating home tab: {traceback.format_exc(e)}")


def send_photo(channel, file, client, log):
    """

    :param channel:
    :param file:
    :param client:
    :param log:
    :return: RESULT OF OPERATION, DICT
    """
    try:
        result = client.files_upload(
            channels=channel,
            file=file,
        )
        log.warning(result)
        return result
    except SlackApiError as e:
        log.error("Error uploading file: {}".format(e))


def send_message(body: str, channel: str, blocks, color: str, client, log):
    """

    :param body:
    :param channel:
    :param blocks:
    :param color:
    :param client:
    :param log:
    :return: RESULT OF OPERATION, DICT
    """
    try:
        if blocks != '':
            result = client.chat_postMessage(
                channel=channel,
                text=f'<@{channel}>, ваш запрос обработан:',
                attachments=json.dumps([{'color': f'#{color}', 'text': f'{body}'}]),
                blocks=blocks
            )
        else:
            result = client.chat_postMessage(
                channel=channel,
                text=f'<@{channel}>, ваш запрос обработан:',
                attachments=json.dumps([{'color': '#FF0000', 'text': f'{body}'}]),
            )
        return result
    except SlackApiError as error:
        log.error(f'API raised an error: {traceback.format_exc(error)}')
