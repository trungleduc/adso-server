#
# Created on Wed Nov 25 2020
# Author : Trung Le
# Email : trung.le@cast2cloud.com
# Copyright (c) 2020 cast2cloud.com , all rights reserved.
#


"""
TODO: Add module docstring
"""

from adso_core import component
from ipywidgets import DOMWidget
from traitlets.traitlets import Unicode, observe, Int
from traitlets.traitlets import List as TList
from traitlets.traitlets import Dict as TDict
import numpy
from typing import Dict, List, TYPE_CHECKING
if TYPE_CHECKING:
    from adso_core.component import Component

module_name = "AdsoLab"
module_version = "0.0.1"
class AdsoLab(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('AdsoModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('AdsoView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    position = Unicode('tab-after').tag(sync=True)
    component = TDict(default_value={}, allow_none=False).tag(sync=True)
    initial_store = TDict(default_value={}, allow_none=False).tag(sync=True)
    update_signal = Int(default_value=0, allow_none=False).tag(sync=True)
    computed_output = TDict(default_value={}, allow_none=False).tag(sync=True)
    server_log = TDict(default_value={}, allow_none=False).tag(sync=True)

    def __init__(self, component: "Component", **kwargs):
        self.position = kwargs.get("position", 'tab-after')
        self._component = component
        self._inputs = []
        self._outputs = []
        lab_mode = kwargs.get("lab_mode", True)
        if lab_mode:
            component.add_callback("adsolab", self.handle_computed_signal)
        self.get_component_data()
        self.on_msg(self.__handle_client_msg)
        self.handle_dict = {"request_run": self.handle_request_run}
        super().__init__(**kwargs)

    def get_component_data(self) -> None:
        self._inputs = [x.to_dict() for x in self._component.input.values()]
        self._outputs = [x.to_dict() for x in self._component.output.values()]
        self.component = {"input": self._inputs, "output": self._outputs}

    def handle_computed_signal(self, **kwarg) -> None:
        result = self._component.get_output()
        for key, value in result.items():
            desc = self._component.output[key].desc
            try:
                len(value)
                if isinstance(value, numpy.ndarray):
                    result[key] = {"value": value.tolist(), "dtype": "ndarray", "desc": desc}
                else:
                    result[key] = {"value": value, "dtype": "List", "desc": desc}
            except:
                result[key] = {"value": value, "dtype": "float", "desc": desc}

        self.computed_output = result
        self.update_signal += 1
        self.server_log = {"msg": "Component executed", "updated": self.update_signal}

    def __handle_client_msg(self, widget, content, buffer):
        print("hello", content)
        action = content["action"]
        payload = content["payload"]
        self.handle_dict[action](payload)

    def handle_request_run(self, payload: Dict) -> None:
        self._component.reset_variable()
        self._component.update_input(payload)
        self._component.execute()
