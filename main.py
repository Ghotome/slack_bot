# -*- coding: utf-8 -*-
import logging
import traceback

import requests
from slack_bolt import App
from slack_sdk import WebClient

import settings
from functions import functions
from views import views

log = logging.getLogger(__name__)
client = WebClient(token=settings.SLACK_BOT_TOKEN)

app = App(
    token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_SIGNING_SECRET
)


@app.event("app_home_opened")
def open_home_tab(event):
    log.warning(event)
    global user
    try:
        client.views_publish(
            user_id=event['user'],
            view=views.render_home_tab()
        )

        user = event['user']

    except Exception as e:
        log.error(f"Error publishing home tab: {traceback.format_exc(e)}")


@app.action('home_page')
def return_to_home_page(ack):
    ack()
    functions.update_home_tab(tab=views.render_home_tab(), user_id=user, client=client, log=log)


@app.action('triggers')
def return_triggers_list(action, ack):
    ack()
    log.warning(action)
    auth = functions.zabbix_login(settings.ZABBIX_API_URL)
    result = functions.get_list_of_triggers(auth)[0]['blocks']
    log.warning(f'User: {user}')

    slack_message = client.chat_postMessage(
        channel=user,
        attachments=[{"color": 'f2c744', 'blocks': result}]
    )
    log.warning(slack_message)


@app.shortcut('ack_problem')
def shortcut_ack_problem(ack, shortcut):
    ack()
    log.warning(shortcut)

    modal_waiting = client.views_open(
        trigger_id=shortcut['trigger_id'],
        view=views.render_empty_modal_sample()
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
    log.warning(result)


@app.action('login_handler')
def send_subscriber_info(ack, action):
    log.warning(action)
    if action['value'].isdecimal():
        log.warning(f'LOGIN: {action["value"]}')
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
        log.warning(result)
        ack()


@app.action('uplinks')
def action_uplinks(ack, action):
    ack()
    log.warning(action)
    image = requests.get(settings.images_links['uplinks'], headers=settings.api_tokens['grafana']['auth']).content
    functions.send_photo(user, image, client=client, log=log)


@app.shortcut('open_modal_speedtests')
def render_modal_speedtests(ack, shortcut):
    ack()
    log.warning(shortcut)
    result = client.views_open(
        trigger_id=shortcut['trigger_id'],
        view=views.render_speedtests_modal()
    )
    log.warning(result)


@app.shortcut('open_modal_user_info')
def render_modal_user_info(ack, shortcut):
    ack()
    log.warning(shortcut)
    result = client.views_open(
        trigger_id=shortcut['trigger_id'],
        view=views.render_input_user_login_modal()
    )
    log.warning(result)


@app.view_submission("")
def action_submission(ack, body):
    ack()
    log.warning(body)
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
        log.warning(result)
    elif "login_input" in body['view']['state']['values'][user_response_key]:
        log.warning(f'Reacted on login input')
        user_input = body['view']['state']['values'][user_response_key]['login_input']['value']
        show_empty_modal = client.views_open(
            trigger_id=trigger_id,
            view=views.render_empty_modal_sample()
        )
        subscriber_data = functions.get_user_info(user_input)
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
        log.warning(result)
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
        problem_update = functions.zabbix_event_acknowledge(auth, message=zbbx_ack_message, event_id=zbbx_trigger_id)
        log.warning(f"CODE: {problem_update} // BODY: {problem_update.content}")
        modal_succes = client.views_open(
            trigger_id=trigger_id,
            view=views.render_modal_success()
        )
        log.warning(modal_succes)


@app.action('fuel')
def action_fuel(ack, action):
    ack()
    log.warning(action)
    image = requests.get(settings.images_links['fuel'],
                         headers=settings.api_tokens['grafana']['auth']).content
    message = functions.send_photo(user, image, client=client, log=log)
    log.warning(message)


@app.action('temp')
def action_fuel(ack, action):
    ack()
    log.warning(action)
    image = requests.get(settings.images_links['temp'],
                         headers=settings.api_tokens['grafana']['auth']).content
    message = functions.send_photo(user, image, client=client, log=log)
    log.warning(message)


@app.action('missed_calls')
def action_missed_calls(ack, action):
    ack()
    log.warning(action)
    image = requests.get(settings.images_links['missed_calls'],
                         headers=settings.api_tokens['grafana']['auth']).content
    message = functions.send_photo(user, image, client=client, log=log)
    log.warning(message)


@app.action('faq')
def action_missed_calls(ack, action):
    ack()
    log.warning(action)
    message_body = views.render_faq_message()
    author = views.render_author()
    result = functions.send_message(channel=user, body=message_body, blocks=author, color='D9EA49', client=client, log=log)
    log.warning(result)


@app.action('call_statistics')
def action_missed_calls(ack, action):
    ack()
    log.warning(action)
    image = requests.get(settings.images_links['calls_statistics'],
                         headers=settings.api_tokens['grafana']['auth']).content
    message = functions.send_photo(user, image, client=client, log=log)
    log.warning(message)


@app.action('callback_statistics')
def action_missed_calls(ack, action):
    ack()
    log.warning(action)
    image = requests.get(settings.images_links['callback_statistics'],
                         headers=settings.api_tokens['grafana']['auth']).content
    message = functions.send_photo(user, image, client=client, log=log)
    log.warning(message)


@app.command("/user_info")
def command_user_info(ack, body):
    ack()
    log.info(body)
    result = client.views_open(
        trigger_id=body['trigger_id'],
        view=views.render_input_user_login_modal()
    )
    log.warning(result)


if __name__ == "__main__":
    app.start()
