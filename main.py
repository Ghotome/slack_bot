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
            view=views.slack_home_tab
        )

        user = event['user']

    except Exception as e:
        log.error(f"Error publishing home tab: {traceback.format_exc(e)}")


@app.action('home_page')
def return_to_home_page(ack):
    ack()
    functions.update_home_tab(tab=views.slack_home_tab, user_id=user, client=client, log=log)


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
        view=views.speedtests_bras_select_modal
    )
    log.warning(result)


@app.shortcut('open_modal_user_info')
def render_modal_user_info(ack, shortcut):
    ack()
    log.warning(shortcut)
    result = client.views_open(
        trigger_id=shortcut['trigger_id'],
        view=views.input_user_login_modal
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
            view=views.empty_modal
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
    message_body = (f"*Основной функционал бота:*\n"
                    f"На главной странице несколько кнопок, это основные и часто используемые запросы.\n"
                    f"\nМеню бота доступно по нажатию на :zap: возле поля для ввода."
                    f"\n\nДоступные взаимодействия с ботом: \n"
                    f"  - Speedtests BRAS - открывает селектор, в котором можно выбрать брас и посмотреть "
                    f"графики speedtest за ним;"
                    f"\n - Информация по логину - открывает окно, в нём нужно ввести логин абонента и в ответ"
                    f"получите основную информацию по нему, есть аналогичная команда."
                    f"\n\nДоступные команды:\n  - /user_info - открывает окно, в котором нужно ввести логин абонента, "
                    f"в ответ получите основную информацию по нему;")
    result = functions.send_message(channel=user, body=message_body, blocks='', color='FF0000', client=client, log=log)
    log.warning(result)


@app.command("/user_info")
def command_user_info(ack, body):
    ack()
    log.info(body)
    result = client.views_open(
        trigger_id=body['trigger_id'],
        view=views.input_user_login_modal
    )
    log.warning(result)


if __name__ == "__main__":
    app.start()
