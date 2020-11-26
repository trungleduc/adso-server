#
# Created on Wed Nov 25 2020
# Author : Trung Le
# Email : trung.le@cast2cloud.com
# Copyright (c) 2020 cast2cloud.com , all rights reserved.
#

from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path(r'ws/notification', consumers.NotificationComsumer.as_asgi()),
]
