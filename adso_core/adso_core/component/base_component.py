#
# Created on Wed Nov 25 2020
# Author : Trung Le
# Email : trung.le@cast2cloud.com
# Copyright (c) 2020 cast2cloud.com , all rights reserved.
#

from typing import Callable, List, Dict, NoReturn, Any, Optional, Union, Tuple
from adso_core.variable import Variable
from collections import OrderedDict
import abc
import numpy
Types = Optional[Union[Any, Tuple[Any, ...]]]


class BaseComponent:

    def __init__(self, name: str, **kwarg) -> None:
        """[summary]

        Args:
            name (str): [description]
        """
        self._name = name
        self._input: OrderedDict[str, Variable] = OrderedDict()
        self._output: OrderedDict[str, Variable] = OrderedDict()
        self._connector: OrderedDict = OrderedDict()
        self._callback: OrderedDict = OrderedDict()
        self.setup(**kwarg)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, val: Any) -> None:
        raise Exception("Can not modify name directly")

    @property
    def input(self) -> OrderedDict:
        """[summary]

        Returns:
            List: [description]
        """
        return self._input

    @input.setter
    def input(self, value: any) -> NoReturn:
        """[summary]

        Args:
            value (any): [description]

        Raises:
            Exception: [description]

        Returns:
            NoReturn: [description]
        """
        raise Exception("Can not modify input directly")

    def add_input(self,
                  name: str,
                  value: Any,
                  unit: str = None,
                  dtype: Types = None,
                  value_range: Union[List, Tuple, numpy.ndarray] = [None, None],
                  desc: str = "") -> None:
        try:
            getattr(self, name)
        except AttributeError:
            self._input[name] = Variable(name, value, unit, dtype, value_range, desc, self.name, True)
            setattr(self, name, self._input[name].value)
        else:
            raise AttributeError(f'variable {name} already exists in component')

    @property
    def output(self) -> OrderedDict:
        """[summary]

        Returns:
            List: [description]
        """
        return self._output

    @output.setter
    def output(self, value: any) -> NoReturn:
        """[summary]

        Args:
            value (any): [description]

        Raises:
            Exception: [description]

        Returns:
            NoReturn: [description]
        """
        raise Exception("Can not modify input directly")

    def add_output(self,
                   name: str,
                   value_range: Union[List, Tuple, numpy.ndarray] = [None, None],
                   desc: str = "") -> None:

        try:
            getattr(self, name)
        except AttributeError:
            self._output[name] = Variable(name, 0., None, Any, value_range, desc, self.name, False)
            setattr(self, name, self._output[name].value)
        else:
            raise AttributeError(f'variable {name} already exists in component')

    def execute(self):
        self.compute()
        for _callback in self._callback.values():
            _callback[0](**_callback[1])

    def add_callback(self, name: str, f: Callable, kwarg: Dict = {}) -> None:
        if name in self._callback:
            return
        else:
            self._callback[name] = [f, kwarg]

    

    def setup(self, **kwargs) -> NoReturn:
        """[summary]

        Returns:
            NoReturn: [description]
        """
        pass


    def compute(self) -> None:
        """[summary]

        Returns:
            NoReturn: [description]
        """
        pass
