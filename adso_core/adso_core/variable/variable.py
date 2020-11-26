#
# Created on Wed Nov 25 2020
# Author : Trung Le
# Email : trung.le@cast2cloud.com
# Copyright (c) 2020 cast2cloud.com , all rights reserved.
#

from typing import Any, Union, List, Tuple, Optional, Dict, _GenericAlias
import numpy
Types = Optional[Union[Any, Tuple[Any, ...]]]
import copy
import logging
logger = logging.getLogger(__name__)

class Variable:
    def __init__(
        self,
        name: str,
        value: Any,
        unit: str = None,
        dtype: Types = None,
        value_range: Union[List, Tuple, numpy.ndarray] = [None, None],
        desc: str = "",
        parent : str = None,
        copy_flag : bool = False,
    ) -> None:
        self.__defaut_value = None
        self._name = name
        self._parent = parent

        if dtype == None:                  
            self._value = value
            self._dtype = type(value)
        else:
            if not dtype is Any and not isinstance(value, dtype):
                raise TypeError(f"{value} and {dtype} are not compatible")
            else:
                self._value = value
                self._dtype = dtype
        if copy_flag: 
            try:
                self.__defaut_value = copy.deepcopy(value) 
            except Exception as e:
                print(e)
                pass  
        self._value_range = value_range
        self._desc = desc
        self._unit = unit

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, val: Any) -> None:
        raise Exception("Can not modify name directly")

    @property
    def parent(self) -> str:
        return self._parent

    @parent.setter
    def parent(self, val: Any) -> None:
        raise Exception("Can not modify parent directly")

    @property
    def dtype(self) -> Types:
        return self._dtype

    @dtype.setter
    def dtype(self, val: Any) -> None:
        raise Exception("Can not modify dtype directly")

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, val) -> None:
        if not self._dtype is Any and not isinstance(val, self._dtype):
            raise TypeError(f"{val} and {self._dtype} are not compatible")
        else:
            self._value = val

    @property
    def value_range(self) -> Union[List, Tuple, numpy.ndarray]:
        return self._value_range

    @value_range.setter
    def value_range(self, val: Any) -> None:
        raise Exception("Can not modify value_range directly")

    @property
    def unit(self) -> str:
        return self._unit

    @unit.setter
    def unit(self, val: Any) -> None:
        raise Exception("Can not modify unit directly")

    @property
    def desc(self) -> str:
        return self._desc

    @desc.setter
    def desc(self, val: str) -> None:
        self._desc = val

    def to_dict(self) -> Dict:
        """[summary]

        Returns:
            Dict: [description]
        """
        ret = {}
        for key in ["name", "desc", "parent", "unit"]:
            ret[key] = getattr(self, key)

        if self.dtype is Any:
            ret["dtype"] = "Any"
        elif isinstance(self.dtype, _GenericAlias):
            ret["dtype"] = str(self.dtype)
        else:
            ret["dtype"] = self.dtype.__name__

        if isinstance(self.value_range, numpy.ndarray):
            ret["value_range"] = self.value_range.tolist()
        else:
            ret["value_range"] = self.value_range

        if self.dtype == numpy.ndarray:
            ret["value"] = self.value.tolist()
        else:
            ret["value"] = self.value

        return ret

    @property
    def default_value(self):
        if self.__defaut_value is not None:
            return copy.deepcopy(self.__defaut_value)
        else:
            logger.info(f"Can not reset variable {self.name}")
            return self._value

    @default_value.setter
    def default_value(self):
        raise Exception("Can not modify default value of variable")