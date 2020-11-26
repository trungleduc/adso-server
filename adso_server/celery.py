#
# Created on Wed Nov 25 2020
# Author : Trung Le
# Email : trung.le@cast2cloud.com
# Copyright (c) 2020 cast2cloud.com , all rights reserved.
#


import importlib
import os
import sys
import numpy
from .adsolab import AdsoLab
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from typing import Dict
from celery import Celery, Task
from .config import ADSO_SERVER_MODE
current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(current_path,"core/adso_model"))
from .core.adso_model import * 


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adso_server.settings')

app = Celery('adso')


app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


def sendMessage(subscriber, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(subscriber, message)


def class_factoty(lab_id):
    model_class = globals().get(lab_id)
    # model_class = lab_module.ModelClass

    class ModelTask(Task):
        _model = None
        name = f"adso_server.celery.ModelTask.{lab_id}"

        def __init__(self, do_init = True) -> None:
            if do_init:
                instance = model_class("lab")
                self.lab_instance = AdsoLab(instance, lab_mode=False)
            
        def run(self, payload, group_id):
            return self.lab_task(payload, group_id)

        def lab_task(self, payload, group_id):

            ret = {'type': 'notify',
                   'action': "computed_output",
                   "payload": None}

            self.lab_instance.handle_request_run(payload)
            result = self.lab_instance._component.get_output()
            for key, value in result.items():
                desc = self.lab_instance._component.output[key].desc
                try:
                    len(value)
                    if isinstance(value, numpy.ndarray):
                        result[key] = {"value": value.tolist(), "dtype": "ndarray", "desc": desc}
                    else:
                        result[key] = {"value": value, "dtype": "List", "desc": desc}
                except:
                    result[key] = {"value": value, "dtype": "float", "desc": desc}
            ret['payload'] = result
            sendMessage(group_id, {'type': 'notify',
                                   'action': "server_log",
                                   "payload": f"Job {self.request.id} computed"})
            sendMessage(group_id, ret)

    return ModelTask


lab_list = ["ProjectileMotion"]
TASK_CLASS: Dict = {}
for lab_id in lab_list:
    TASK_CLASS[lab_id] = class_factoty(lab_id)
    app.register_task(TASK_CLASS[lab_id])


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
