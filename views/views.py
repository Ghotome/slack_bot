import json
import traceback


def render_faq_message():
    message_body = (f"*Основной функционал бота:*\n"
                    f"На главной странице несколько кнопок, это основные и часто используемые запросы.\n"
                    f"\n_*Как попасть в меню бота:*_"
                    f"\n*[Для PC]* _Меню бота доступно по нажатию на_ :zap: _возле поля для ввода_"
                    f"\n*[Для телефонов]* _Меню бота доступно по нажатию на_ :heavy_plus_sign: -> *Быстрые действия*"
                    f"\n\n*Доступные взаимодействия с ботом:* \n"
                    f"  - _*Speedtests BRAS*_ - открывает селектор, в котором можно выбрать брас и посмотреть "
                    f"графики speedtest за ним;"
                    f"\n - _*Информация по логину*_ - открывает окно, в нём нужно ввести логин абонента и в ответ"
                    f"получите основную информацию по нему, есть аналогичная команда."
                    f"\n - _*Обновить проблему *_- открывает окно, где нужно выбрать одну из текущих проблем, "
                    f"обязательно ввести комментарий и нажать _*Готово*_. "
                    f"Предназначено для подтвверждения и добавления комментариев к проблеме в Zabbix."
                    f"\n_*ВАЖНО*: функция подтверждения проблем работает не у всех, а только у админов, саппортов "
                    f"и монтажников с доступами на узлы._"
                    f"\n\nДоступные команды:\n  - _*/user_info*_ - открывает окно, в котором нужно ввести логин абонента, "
                    f"в ответ получите основную информацию по нему;")
    return message_body


def render_home_tab():
    slack_home_tab = json.dumps(
        {
            "type": "home",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "DiaNet BOT -- Главное меню\nВоспользуйтесь одним из блоков ниже"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ("_Помимо указанных здесь данных, дополнительный функционал находится в меню бота._\n"
                                 "_Информация о том, как получить доступ к меню, находится в разделе *FAQ*._\n"
                                 "_*ВАЖНО*_ *-- изображения графана рендерит в районе 10 секунд, тыкать кучу раз по "
                                 "кнопкам не нужно!*\n"
                                 "_*ВАЖНО*_ *-- иногда заббикс отвечает 5-10 секунд, если список триггеров не пришёл, "
                                 "попробуйте запросить ещё раз.*\n"
                                 "_*ВАЖНО*_ *-- подтверждение проблем реализовано пока что только через отдельное "
                                 "меню бота(см. раздел _FAQ_), кнопка 'Подтвердить проблему' отправит вас на заббикс. "
                                 "У кого нет туда доступа(монтажники, например), могут подтверждать отсюда, с пмощью "
                                 "функционала бота.*")
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*_Метрики систем мониторинга на узлах_*\n"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Триггеры"
                            },
                            "style": "primary",
                            "value": "click_me_123",
                            "action_id": "triggers"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Уровень топлива"
                            },
                            "style": "primary",
                            "value": "click_me_123",
                            "action_id": "fuel"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Температура"
                            },
                            "style": "primary",
                            "value": "click_me_123",
                            "action_id": "temp"
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*_Данные мониторинга, графики, информация для саппортов и админов_*"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Триггеры"
                            },
                            "style": "primary",
                            "value": "click_me_123",
                            "action_id": "triggers"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Аплинки"
                            },
                            "style": "primary",
                            "value": "click_me_123",
                            "action_id": "uplinks"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Пропущенные"
                            },
                            "style": "primary",
                            "value": "click_me_123",
                            "action_id": "missed_calls"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Статистика по звонкам"
                            },
                            "style": "primary",
                            "value": "click_me_123",
                            "action_id": "call_statistics"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Статистика по коллбекам"
                            },
                            "style": "primary",
                            "value": "click_me_123",
                            "action_id": "callback_statistics"
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*_Раздел FAQ_*"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": (f"*Основной функционал бота:*\n"
                                 f"На главной странице несколько кнопок, это основные и часто используемые запросы.\n"
                                 f"\n_*Как попасть в меню бота:_*"
                                 f"\n*[Для PC]* _Меню бота доступно по нажатию на_ :zap: _возле поля для ввода_"
                                 f"\n*[Для телефонов]* _Меню бота доступно по нажатию на_ :heavy_plus_sign: -> *Быстрые действия*"
                                 f"\n\n*Доступные взаимодействия с ботом:* \n"
                                 f"  - _*Speedtests BRAS*_ - открывает селектор, в котором можно выбрать брас и посмотреть "
                                 f"графики speedtest за ним;"
                                 f"\n - _*Информация по логину*_ - открывает окно, в нём нужно ввести логин абонента и в ответ"
                                 f"получите основную информацию по нему, есть аналогичная команда."
                                 f"\n - _*Обновить проблему *_- открывает окно, где нужно выбрать одну из текущих проблем, "
                                 f"обязательно ввести комментарий и нажать _*Готово*_. "
                                 f"Предназначено для подтвверждения и добавления комментариев к проблеме в Zabbix."
                                 f"\n_*ВАЖНО*: функция подтверждения проблем работает не у всех, а только у админов, саппортов "
                                 f"и монтажников с доступами на узлы._"
                                 f"\n\nДоступные команды:\n  - _*/user_info*_ - открывает окно, в котором нужно ввести логин абонента, "
                                 f"в ответ получите основную информацию по нему;"
                                 '\n_*Если нужно что-то добавить/убрать или остались вопросы, спросите отдел эксплуатации.*_')
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "FAQ"
                            },
                            "style": "primary",
                            "value": "click_me_123",
                            "action_id": "faq"
                        }
                    ]
                },
                {
                    "type": "divider"
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain_text",
                            "text": "Developed by Egor Nefedov"
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
                    },
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain_text",
                            "text": "Developed by Egor Nefedov"
                        }
                    ]
                }
            ]
        }
    )
    return speedtests_bras_select_modal


def render_modal_waiting():
    empty_modal = json.dumps(
        {
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": "DiaNet"
            },
            "close": {
                "type": "plain_text",
                "text": "Закрыть"
            },
            "blocks": [
                {
                    "type": "divider"
                },
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
                            "text": "Должно быть быстро"
                        }
                    ]
                },
                {
                    "type": "divider"
                }
            ]
        }
    )
    return empty_modal


def render_author():
    author = json.dumps(
        [
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": "Developed by Egor Nefedov",
                        "emoji": True
                    }
                ]
            }
        ]
    )
    return author


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
    try:
        for item in problems:
            result['options'].append(
                {
                    "text": {
                        "type": "plain_text",
                        "text": f"{item}"[:74],
                        "emoji": True
                    },
                    "value": f"{problems[item]}"
                }
            )
        return result
    except Exception as error:
        return traceback.format_exc(error)


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
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain_text",
                            "text": "Developed by Egor Nefedov"
                        }
                    ]
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
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "plain_text",
                            "text": "Developed by Egor Nefedov and Ivan Golubev"
                        }
                    ]
                }
            ]
        }
    )
    return user_info_modal
