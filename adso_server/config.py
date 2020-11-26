#
# Created on Wed Nov 25 2020
# Author : Trung Le
# Email : trung.le@cast2cloud.com
# Copyright (c) 2020 cast2cloud.com , all rights reserved.
#


import os

ADSO_SERVER_MODE = os.environ.get('ADSO_SERVER_MODE', 'server')
REDIS_URL = os.environ.get('REDIS_URL', '127.0.0.1') # 'redis://redis:6379/0')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379') # 'redis://redis:6379/0')
