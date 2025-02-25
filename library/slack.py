import requests
from ansible.plugins.callback import CallbackBase

class CallbackBase:
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = "notification"
    CALLBACK_NAME = "slack_notify"
    CALLBACK_NEEDS_WHITELIST = True

    def v2_playbook_on_stats(self, stats):
        message = {
            "text": "Ansible Playbook Finished",
            "attachments": [
                {
                    "fields": [
                        {"title": "Hosts Processed", "value": str(len(stats.processed.keys())), "short": True},
                        {"title": "Hosts Failed", "value": str(len(stats.failures.keys())), "short": True},
                    ]
                }
            ]
        }

        webhook_url = "https://hooks.slack.com/services/XXXXXXXX/XXXXXXXX/XXXXXXXXX"
        requests.post(webhook_url, json=message)



