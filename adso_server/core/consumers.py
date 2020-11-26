#
# Created on Wed Nov 25 2020
# Author : Trung Le
# Email : trung.le@cast2cloud.com
# Copyright (c) 2020 cast2cloud.com , all rights reserved.
#

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
import datetime
import logging
from rest_framework.authtoken.models import Token
from .adso_model import *
from ..adsolab import AdsoLab
from ..celery import  TASK_CLASS

log = logging.getLogger("adso")


def sendMessage(subscriber, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(subscriber, message)


class NotificationComsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        log.debug("Websocket client connected [%s]", self.channel_name)
        self.lab_instance = None
        self.send(text_data=json.dumps({
            "action": "HANDSHAKE",
            "payload": {
                "serverTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z"),
                "msg": "Hello from ADSO-SERVER"
            }

        }))

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        typeData = text_data_json['action']
        payload = text_data_json['payload']
        if typeData == "Authentication":
            token = payload["token"]
            self.lab_id = payload["modelID"]
            try:
                user = Token.objects.get(key=token).user
                self.user_private_channel = f"private_channel-user-{user.id}-{user.username}"
                log.debug(
                    f"Adding connection {self.channel_name} to user's private channel {self.user_private_channel}")
                async_to_sync(self.channel_layer.group_add)(
                    self.user_private_channel,
                    self.channel_name
                )
                try:
                    self.model_class = globals().get(self.lab_id)
                    instance = self.model_class("lab")
                    self.lab_instance = AdsoLab(instance, lab_mode=False)
                    content = self.lab_instance.component

                    self.send(text_data=json.dumps({
                        'action': "MODEL_COMPONENT",
                        "payload": content
                    }))
                except Exception as e:
                    log.debug(e)
                    self.close()

            except Token.DoesNotExist:
                self.close()
        elif typeData == "request_run":
            if self.lab_instance is None:
                self.close()
            task_id = TASK_CLASS[self.lab_id](False).delay(payload, self.user_private_channel)
            server_log = f'Job with ID {task_id} submitted'
            self.send(text_data=json.dumps({
                'action': "server_log",
                "payload": server_log
            }))
        else:
            self.close()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.user_private_channel,
            self.channel_name
        )

    def notify(self, message):
        del message["type"]
        self.send(json.dumps(message))
