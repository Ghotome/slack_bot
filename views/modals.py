import json

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

get_user_info_modal = json.dumps(
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