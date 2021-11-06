import json


def render_faq_message():
    message_body = (f"*Основной функционал бота:*\n"
                    f"На главной странице несколько кнопок, это основные и часто используемые запросы.\n"
                    f"\nМеню бота доступно по нажатию на :zap: возле поля для ввода(если с ПК)"
                    f"\n\nДоступные взаимодействия с ботом: \n"
                    f"  - Speedtests BRAS - открывает селектор, в котором можно выбрать брас и посмотреть "
                    f"графики speedtest за ним;"
                    f"\n - Информация по логину - открывает окно, в нём нужно ввести логин абонента и в ответ"
                    f"получите основную информацию по нему, есть аналогичная команда."
                    f"\n - Обновить прооблему - открывает окно, где нужно выбрать одну из текущих проблем, "
                    f"обязательно ввести комментарий и нажать '_*Готово*_'. "
                    f"Предназначено для подтвверждения и добавления комментариев к проблеме в Zabbix."
                    f"\n_*ВАЖНО*: функция работает не у всех, а только админов, саппортов и монтажников с доступами на узлы._"
                    f"\n\nДоступные команды:\n  - /user_info - открывает окно, в котором нужно ввести логин абонента, "
                    f"в ответ получите основную информацию по нему;")
    return message_body


def render_home_tab():
    slack_home_tab = json.dumps(
    {
        "type": "home",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ("*Cамые часто используемыые функции*\n"
                             "*Для получения более подробной информации о функционале бота, нажмите на _FAQ_*")
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
                            "text": "Уровень топлива",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": "click_me_123",
                        "action_id": "fuel"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Температура",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": "click_me_123",
                        "action_id": "temp"
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
                            "text": "FAQ",
                            "emoji": True
                        },
                        "style": "primary",
                        "value": "click_me_123",
                        "action_id": "faq"
                    }
                ]
            }
        ]
    }
    )
    return slack_home_tab


def render_input_user_login_modal():
    input_user_login_modal = json.dumps(
    {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Информация об абоненте ",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Готово",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Отмена",
            "emoji": True
        },
        "blocks": [
            {
                "dispatch_action": True,
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "login_input"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Введите логин",
                    "emoji": True
                }
            }
        ]
    }
    )
    return input_user_login_modal


def render_speedtests_modal():
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
    return speedtests_bras_select_modal


def render_empty_modal_sample():
    empty_modal = json.dumps(
    {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "DiaNet",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Закрыть",
            "emoji": True
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":hourglass:*Ожидайте, запрос обрабатывается*"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": "Должно быть быстро",
                        "emoji": True
                    }
                ]
            }
        ]
    }
    )
    return empty_modal


def render_empy_blocks_sample():
    empty_blocks = {
    "blocks": [
    ]
}
    return empty_blocks


def render_modal_success():
    modal_success = json.dumps(
    {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "DiaNet ZABBIX",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Закрыть",
            "emoji": True
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":white_check_mark:_*Success*_"
                }
            }
        ]
    }
    )
    return modal_success


def render_options_problems_to_ack(problems):
    result = {
        "options": []
    }
    for item in problems:
        result['options'].append(
            {
                "text": {
                    "type": "plain_text",
                    "text": f"{item}",
                    "emoji": True
                },
                "value": f"{problems[item]}"
            }
        )
    return result


def render_ack_problem_modal(options):
    zabbix_problems_ack_modal = json.dumps(
        {
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": "DiaNet ZABBIX",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Готово",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Отмена",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "input",
                    "element": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Выберите проблему для подтверждения",
                            "emoji": True
                        },
                        "options": options['options'],
                        "action_id": "problems_to_ack"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Текущие проблемы",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "problems_to_ack_message"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Введите сообщение",
                        "emoji": True
                    }
                }
            ]
        }
    )
    return zabbix_problems_ack_modal


def render_one_trigger_line(trigger: str, link: str, additional_message: str = ''):
    one_trigger_line = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"<{link}|{trigger}>\r{additional_message}"
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Обновить проблему",
                "emoji": True
            },
            "value": "not_an_action",
            "action_id": "not_an_action",
            "url": f"{link}"
        }
    }
    return one_trigger_line


def render_user_info_modal(body, subscriber):
    user_info_modal = json.dumps(
        {
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": f"Абонент {subscriber}",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Закрыть",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{body}"
                    }
                }
            ]
        }
    )
    return user_info_modal