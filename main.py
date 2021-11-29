# -*- coding: utf-8 -*-
import datetime
import logging
import time
import traceback

import requests
from slack_bolt import App
from slack_sdk import WebClient

import settings
from functions import functions
from views import views

if settings.DEBUG:
    log = logging.getLogger(__name__)
    log_file = open(settings.log_file, 'a')

client = WebClient(token=settings.SLACK_BOT_TOKEN)

app = App(
    token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_SIGNING_SECRET
)


@app.event("app_home_opened")
def open_home_tab(event):
    global user
    user = event['user']
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- "
                       f"JSON ACK - - HOME TAB OPENED: \n{event}")
    try:
        client.views_publish(
            user_id=event['user'],
            view=views.render_home_tab()
        )

    except Exception as e:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                  f"Error publishing home tab: {traceback.format_exc(e)}")


@app.action('triggers')
def return_triggers_list(action, ack):
    ack()
    log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                    f"USER: {user}, {settings.operators[user]['name']} -- "
                    f"JSON ACK - - TRIGGERS: \n{action}")
    auth = functions.zabbix_login(settings.ZABBIX_API_URL)
    result = functions.get_list_of_triggers(auth)[0]['blocks']
    slack_message = client.chat_postMessage(
        channel=user,
        attachments=[{"color": 'f2c744', 'blocks': result}]
    )
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- "
                       f"JSON MESSAGE - - TRIGGERS: \n{slack_message}")


@app.shortcut('ack_problem')
def shortcut_ack_problem(ack, shortcut):
    ack()
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                    f"USER: {user}, {settings.operators[user]['name']} -- "
                       f"JSON ACK - - ACK PROBLEM: \n{shortcut}")

    modal_waiting = client.views_open(
        trigger_id=shortcut['trigger_id'],
        view=views.render_modal_waiting()
    )
    view_id = modal_waiting['view']['id']
    auth = functions.zabbix_login(settings.ZABBIX_API_URL)
    problems = functions.get_list_of_triggers(auth)[1]
    options = views.render_options_problems_to_ack(problems)
    modal = views.render_ack_problem_modal(options)
    result = client.views_update(
        view_id=view_id,
        view=modal
    )
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- "
                       f"JSON MODAL VIEW - - ACK PROBLEM: \n{result}")


@app.action('login_handler')
def send_subscriber_info(ack, action):
    log.warning(action)
    if action['value'].isdecimal():
        if settings.DEBUG:
            log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                           f"USER: {user}, {settings.operators[user]['name']} -- "
                           f"LOGIN DEFINED BY USER INPUT: {action['value']}")
        subscriber_data = functions.get_user_info(str(action['value']))
        log.warning(subscriber_data)
        message_body = (f"*Логин:* {action['value']}\n"
                        f"*ФИО:* {subscriber_data['fio']}\n"
                        f"*Статус учётки:* {subscriber_data['subscriber_status']}\n"
                        f"*Адрес:* {subscriber_data['address']}\n"
                        f"*Тариф:* {subscriber_data['tariff']}\n"
                        f"*Статус услуги:* {subscriber_data['status']}\n"
                        f"*Статус ОНУ:* {subscriber_data['onu_status']}\n"
                        f"*Показания ОНУ:* {subscriber_data['onu_attenuation']}\n"
                        f"*Позиция ОНУ:* {subscriber_data['onu_position']}\n")
        result = functions.send_message(body=message_body, channel=user, blocks='', color='00FFF7', client=client,
                                        log=log)
        if settings.DEBUG:
            log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                           f"USER: {user}, {settings.operators[user]['name']} -- "
                           f"JSON MESSAGE - - LOGIN HANDLER: \n{result}")
        ack()


@app.action('uplinks')
def action_uplinks(ack, action):
    ack()
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- "
                       f"JSON ACK - - UPLINKS: \n{action}")
    image = requests.get(settings.images_links['uplinks'], headers=settings.api_tokens['grafana']['auth']).content
    send_photo = functions.send_photo(user, image, client=client, log=log)
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- "
                       f"JSON SEND PHOTO - - UPLINKS: \n{send_photo}")


@app.shortcut('open_modal_speedtests')
def render_modal_speedtests(ack, shortcut):
    ack()
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- "
                       f"JSON ACK SHORTCUT - - MODAL SPEEDTESTS CHOSE: \n{shortcut}")
    result = client.views_open(
        trigger_id=shortcut['trigger_id'],
        view=views.render_speedtests_modal()
    )
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- "
                       f"JSON MODAL RENDER - - SPEEDTESTS CHOSE: \n{result}")


@app.shortcut('open_modal_user_info')
def render_modal_user_info(ack, shortcut):
    ack()
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- "
                       f"JSON SHORTCUT - - RENDER MODAL LOGIN INPUT: \n{shortcut}")
    result = client.views_open(
        trigger_id=shortcut['trigger_id'],
        view=views.render_input_user_login_modal()
    )
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- "
                       f"JSON MODAL RENDER - - USER LOGIN INPUT: \n{result}")


@app.view_submission("")
def action_submission(ack, body):
    ack()
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"JSON ACK SUBMISSION - - \n{body}")
    user_id = body['user']['id']
    trigger_id = body['trigger_id']
    user_response_key = list(body['view']['state']['values'])[-1]
    if "select_bras_speedtest" in body['view']['state']['values'][user_response_key]:
        log.warning(f'Reacted speedtests request')
        user_choise = \
            body['view']['state']['values'][user_response_key]['select_bras_speedtest']['selected_option']['text'][
                'text']
        image = requests.get(settings.images_links['speedtests'].format(user_choise),
                             headers=settings.api_tokens['grafana']['auth']).content
        result = functions.send_photo(user_id, image, client=client, log=log)
        if settings.DEBUG:
            log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                           f"JSON SEND PHOTO - - SPEEDTEST BRAS: \n{result}")
    elif "login_input" in body['view']['state']['values'][user_response_key]:
        user_input = body['view']['state']['values'][user_response_key]['login_input']['value']
        show_empty_modal = client.views_open(
            trigger_id=trigger_id,
            view=views.render_modal_waiting()
        )
        subscriber_data = functions.get_user_info(user_input)
        log.warning(f'Get info by login {user_input}: \n{subscriber_data}')
        message_body = (f"*Логин:* {user_input}\n"
                        f"*ФИО:* {subscriber_data['fio']}\n"
                        f"*Статус учётки:* {subscriber_data['subscriber_status']}\n"
                        f"*Адрес:* {subscriber_data['address']}\n"
                        f"*Тариф:* {subscriber_data['tariff']}\n"
                        f"*Статус услуги:* {subscriber_data['status']}\n"
                        f"*Статус ОНУ:* {subscriber_data['onu_status']}\n"
                        f"*Показания ОНУ:* {subscriber_data['onu_attenuation']}\n"
                        f"*Позиция ОНУ:* {subscriber_data['onu_position']}\n")
        user_info_modal = views.render_user_info_modal(message_body, user_input)
        view_id = show_empty_modal['view']['id']
        result = client.views_update(
            view_id=view_id,
            view=user_info_modal
        )
        if settings.DEBUG:
            log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                           f"JSON MODAL RENDER - - USER INFO BY LOGIN: \n{result}")
    elif len(list(body['view']['state']['values'])) == 2:
        auth = functions.zabbix_login(settings.ZABBIX_API_URL)
        problem_values_key = list(body['view']['state']['values'])[0]
        message_key = list(body['view']['state']['values'])[1]
        trigger_id = body['trigger_id']
        user_name = 'Неизвестный пользователь'
        for user in settings.operators:
            if user == user_id:
                user_name = settings.operators[user]['name']
                break
            else:
                user_name = 'Неизвестный пользователь'

        zbbx_trigger_id = body['view']['state']['values'][problem_values_key]['problems_to_ack']['selected_option'][
            'value']
        zbbx_ack_message = f"{user_name}: {body['view']['state']['values'][message_key]['problems_to_ack_message']['value']}"
        modal_waiting = client.views_open(
            trigger_id=trigger_id,
            view=views.render_modal_waiting()
        )
        view_id = modal_waiting['view']['id']
        problem_update = functions.zabbix_event_acknowledge(auth, message=zbbx_ack_message, event_id=zbbx_trigger_id)
        if settings.DEBUG:
            log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                           f"CODE: {problem_update} // BODY: {problem_update.content}")
        client.views_update(
            view_id=view_id,
            view=views.render_modal_success()
        )


@app.action('fuel')
def action_fuel(ack, action):
    ack()
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSON ACK - - FUEL LEVEL: \n{action}")
    image = requests.get(settings.images_links['fuel'],
                         headers=settings.api_tokens['grafana']['auth']).content
    message = functions.send_photo(user, image, client=client, log=log)
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSON SEND PHOTO - - FUEL LEVEL: \n{message}")


@app.action('temp')
def action_fuel(ack, action):
    ack()
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSON ACK - - TEMPERATURE: \n{action}")
    image = requests.get(settings.images_links['temp'],
                         headers=settings.api_tokens['grafana']['auth']).content
    message = functions.send_photo(user, image, client=client, log=log)
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSON SEND PHOTO - - TEMPERATURE: \n{message}")


@app.action('missed_calls')
def action_missed_calls(ack, action):
    ack()
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSON ACK - MISSED CALLS: \n{action}")
    image = requests.get(settings.images_links['missed_calls'],
                         headers=settings.api_tokens['grafana']['auth']).content
    message = functions.send_photo(user, image, client=client, log=log)
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSON SEND PHOTO - - MISSED CALLS: \n{message}")


@app.action('faq')
def action_missed_calls(ack, action):
    ack()
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSON ACK - - FAQ: \n{action}")
    message_body = views.render_faq_message()
    author = views.render_author()
    result = functions.send_message(channel=user, body=message_body,
                                    blocks=author, color='D9EA49',
                                    client=client, log=log)
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSON SENDD MESSAGE - - FAQ: \n{result}")


@app.action('call_statistics')
def action_missed_calls(ack, action):
    ack()
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSON ACK - - CALL STATISTICS: \n{action}")
    image = requests.get(settings.images_links['calls_statistics'],
                         headers=settings.api_tokens['grafana']['auth']).content
    message = functions.send_photo(user, image, client=client, log=log)
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSON SEND PHOTO - - CALL STATISTICS: \n{message}")


@app.action('callback_statistics')
def action_missed_calls(ack, action):
    ack()
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSON ACK - - CALLBACK STATISTICS: \n{action}")
    image = requests.get(settings.images_links['callback_statistics'],
                         headers=settings.api_tokens['grafana']['auth']).content
    message = functions.send_photo(user, image, client=client, log=log)
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSON SEND PHOTO - - CALLBACK STATISTICS: \n{message}")


@app.command("/user_info")
def command_user_info(ack, body):
    ack()
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSON COMMAND - - USER_INFO: \n{body}")
    result = client.views_open(
        trigger_id=body['trigger_id'],
        view=views.render_input_user_login_modal()
    )
    if settings.DEBUG:
        log_file.write(f"\n\n[{datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%m:%S')}] - - "
                       f"USER: {user}, {settings.operators[user]['name']} -- JSOM MODAL RENDER - - USER INFO: \n{result}")


if __name__ == "__main__":
    app.start()
