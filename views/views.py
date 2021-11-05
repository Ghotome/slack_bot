import json

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

empty_blocks = {
    "blocks": [
    ]
}

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
                        "type": "default",
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
            "text": f":warning:<{link}|{trigger}>\r{additional_message}"
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
