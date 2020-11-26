#
# Created on Wed Nov 25 2020
# Author : Trung Le
# Email : trung.le@cast2cloud.com
# Copyright (c) 2020 cast2cloud.com , all rights reserved.
#

from .celery import app as celery_app

__all__ = ('celery_app',)
