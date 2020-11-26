#
# Created on Wed Nov 25 2020
# Author : Trung Le
# Email : trung.le@cast2cloud.com
# Copyright (c) 2020 cast2cloud.com , all rights reserved.
#

import os
import importlib
def import_all():
  all_module = []
  globals_, locals_ = globals(), locals()
  for fileName in os.listdir(os.path.dirname(__file__)):
    if fileName not in ["__pycache__","__init__.py" ]:
      try:
          mdl = importlib.import_module(fileName)
          names = mdl.__dict__["__all__"]
          all_module = all_module + names
          globals().update({k: getattr(mdl, k) for k in names})
      except Exception as err:
          raise err

  return all_module


__all__ = import_all()