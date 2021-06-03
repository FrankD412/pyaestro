"""Package-wide utility base classes that all submodules can use."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, Type, TypeVar


T = TypeVar("T", bound="Specifiable")


class Serializable(ABC):
    """An abstract API denoting a class' ability to be serialized."""
    
    @abstractmethod
    def serialize(self) -> dict:
        """Generate a serialized dictionary of the class instance.

        Returns:
            dict: A specification dictionary representing the object instance.
        """
        ...


class Specifiable(ABC):
    """An abstract API for classes that can be specified by a dictionary."""
    
    @classmethod
    @abstractmethod
    def from_specification(cls: Type[T], specification:Dict) -> T:
        """Creates an instance of a class from a specification dictionary.

        Args:
            specification (Dict): A specification of the instance to be created.

        Returns:
            Specifiable: An instance of the Specifiable class.
        """
        ...