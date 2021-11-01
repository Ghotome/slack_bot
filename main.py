# -*- coding: utf-8 -*-
import json
import logging
import traceback

import requests
from slack_bolt import App
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import settings

log = logging.getLogger(__name__)
client = WebClient(token=settings.SLACK_BOT_TOKEN)

app = App(
    token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_SIGNING_SECRET,
)


def zabbix_login(url: str):
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


def update_home_tab(tab, user_id):
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


def send_photo(channel, file):
    try:
        result = client.files_upload(
            channels=channel,
            file=file,
        )
        log.warning(result)
        return result
    except SlackApiError as e:
        log.error("Error uploading file: {}".format(e))


@app.event("app_home_opened")
def open_home_tab(event):
    log.warning(event)
    global user
    try:
        client.views_publish(
            user_id=event['user'],
            view=settings.slack_home_tab
        )

        user = event['user']

    except Exception as e:
        log.error(f"Error publishing home tab: {traceback.format_exc(e)}")


@app.action('home_page')
def return_to_home_page(ack):
    ack()
    update_home_tab(tab=settings.slack_home_tab, user_id=user)


def send_message(body: str, channel: str, blocks, color: str):
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


@app.action('triggers')
def return_triggers_list(action, ack):
    ack()
    log.warning(action)
    auth = zabbix_login(settings.ZABBIX_API_URL)
    result = settings.get_list_of_triggers(auth)
    log.warning(f'User: {user}')
    slack_message = send_message(body=result, channel=user, blocks='', color='0013FF')
    log.warning(slack_message)


@app.action('login_handler')
def send_subscriber_info(ack, action):
    log.warning(action)
    if action['value'].isdecimal():
        log.warning(f'LOGIN: {action["value"]}')
        subscriber_data = settings.get_user_info(str(action['value']))
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
        result = send_message(body=message_body, channel=user, blocks='', color='00FFF7')
        log.warning(result)
        ack()


@app.action('uplinks')
def action_uplinks(ack, action):
    ack()
    log.warning(action)
    image = requests.get(settings.images_links['uplinks'], headers=settings.api_tokens['grafana']['auth']).content
    send_photo(user, image)


@app.shortcut('open_modal_speedtests')
def render_modal_speedtests(ack, shortcut):
    ack()
    log.warning(shortcut)
    result = client.views_open(
        trigger_id=shortcut['trigger_id'],
        view=settings.speedtests_bras_select_modal
    )
    log.warning(result)


@app.view_submission("")
def action_speedtest(ack, body):
    ack()
    log.warning(body)
    user_id = body['user']['id']
    user_response_key = list(body['view']['state']['values'])[-1]
    if body['view']['state']['values'][user_response_key]['select_bras_speedtest']:
        user_choise = \
            body['view']['state']['values'][user_response_key]['select_bras_speedtest']['selected_option']['text']['text']
        image = requests.get(settings.images_links['speedtests'].format(user_choise),
                             headers=settings.api_tokens['grafana']['auth']).content
        result = send_photo(user_id, image)
        log.warning(result)


@app.action('fuel')
def action_fuel(ack, action):
    ack()
    log.warning(action)
    image = requests.get(settings.images_links['fuel'],
                         headers=settings.api_tokens['grafana']['auth']).content
    message = send_photo(user, image)
    log.warning(message)


@app.action('missed_calls')
def action_missed_calls(ack, action):
    ack()
    log.warning(action)
    image = requests.get(settings.images_links['missed_calls'],
                         headers=settings.api_tokens['grafana']['auth']).content
    message = send_photo(user, image)
    log.warning(message)


@app.action('faq')
def action_missed_calls(ack, action):
    ack()
    log.warning(action)
    message_body = (f"Основной функционал бота:\n"
                    f"На главвной странице несколько кнопок, они возвращают в личку то, что на них написано\n"
                    f"В меню бота так же есть несколько кнопок, та 01.11.21 - только Speedtest")
    result = send_message(channel=user, body=message_body, blocks='', color='FF0000')
    log.warning(result)


if __name__ == "__main__":
    app.start()
