# -*- coding: utf-8 -*-
import logging
import traceback
from views import modals
from functions import functions
import requests
from slack_bolt import App
from slack_sdk import WebClient
import settings

log = logging.getLogger(__name__)
client = WebClient(token=settings.SLACK_BOT_TOKEN)

app = App(
    token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_SIGNING_SECRET,
)


@app.event("app_home_opened")
def open_home_tab(event):
    log.warning(event)
    global user
    try:
        client.views_publish(
            user_id=event['user'],
            view=modals.slack_home_tab
        )

        user = event['user']

    except Exception as e:
        log.error(f"Error publishing home tab: {traceback.format_exc(e)}")


@app.action('home_page')
def return_to_home_page(ack):
    ack()
    functions.update_home_tab(tab=modals.slack_home_tab, user_id=user, client=client, log=log)


@app.action('triggers')
def return_triggers_list(action, ack):
    ack()
    log.warning(action)
    auth = functions.zabbix_login(settings.ZABBIX_API_URL)
    result = functions.get_list_of_triggers(auth)
    log.warning(f'User: {user}')
    slack_message = functions.send_message(body=result, channel=user, blocks='', color='0013FF', client=client, log=log)
    log.warning(slack_message)


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
        result = functions.send_message(body=message_body, channel=user, blocks='', color='00FFF7', client=client, log=log)
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
        view=modals.speedtests_bras_select_modal
    )
    log.warning(result)


@app.shortcut('open_modal_user_info')
def render_modal_user_info(ack, shortcut):
    ack()
    log.warning(shortcut)
    result = client.views_open(
        trigger_id=shortcut['trigger_id'],
        view=modals.get_user_info_modal
    )
    log.warning(result)


@app.view_submission("")
def action_submission(ack, body):
    ack()
    log.warning(body)
    user_id = body['user']['id']
    user_response_key = list(body['view']['state']['values'])[-1]
    if body['view']['state']['values'][user_response_key]['select_bras_speedtest']:
        user_choise = \
            body['view']['state']['values'][user_response_key]['select_bras_speedtest']['selected_option']['text']['text']
        image = requests.get(settings.images_links['speedtests'].format(user_choise),
                             headers=settings.api_tokens['grafana']['auth']).content
        result = functions.send_photo(user_id, image, client=client, log=log)
        log.warning(result)
    elif body['view']['state']['values'][user_response_key]['login_input']:
        user_input = body['view']['state']['values'][user_response_key]['login_input']['value']
        message_body = functions.get_user_info(user_input)
        log.warning(message_body)
        result = functions.send_message(message_body, user_input, client=client, log=log, color='000FFF', blocks='')
        log.warning(result)


@app.action('fuel')
def action_fuel(ack, action):
    ack()
    log.warning(action)
    image = requests.get(settings.images_links['fuel'],
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
    message_body = (f"*Основной функционал бота:*\n"
                    f"На главной странице несколько кнопок, они возвращают в личку то, что на них написано\n"
                    f"В меню бота так же есть несколько кнопок, та 01.11.21 - только Speedtest"
                    f"\nМеню бота доступно по нажатию на :zap: возле поля для ввода.")
    result = functions.send_message(channel=user, body=message_body, blocks='', color='FF0000', client=client, log=log)
    log.warning(result)


if __name__ == "__main__":
    app.start()
