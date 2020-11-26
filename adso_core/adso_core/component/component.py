#
# Created on Wed Nov 25 2020
# Author : Trung Le
# Email : trung.le@cast2cloud.com
# Copyright (c) 2020 cast2cloud.com , all rights reserved.
#

from .base_component import BaseComponent
from typing import Dict
import numpy


class Component(BaseComponent):

    def __init__(self, name: str, **kwarg) -> None:

        super().__init__(name, **kwarg)

    def update_input(self, payload: Dict) -> None:
        for key, val in payload.items():
            component = key.split(".")[0]
            var_name = key.split(".")[1]
            value = val["value"]
            dtype = val["dtype"]
            if component == self.name:
                if dtype == "ndarray":
                    setattr(self, var_name, numpy.array(value[0]))
                else:
                    setattr(self, var_name, value)

    def reset_variable(self) -> None:
        for key, val in self._input.items():
            setattr(self, key, val.default_value)

    def get_output(self) -> Dict:
        ret = {}
        for key in self._output:
            ret[key] = getattr(self, key)

        return ret
