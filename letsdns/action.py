# Copyright © 2022 Ralph Seichter
#
# This file is part of LetsDNS.
#
# LetsDNS is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# LetsDNS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with LetsDNS.
# If not, see <https://www.gnu.org/licenses/>.
from abc import ABC
from abc import abstractmethod
from typing import Type

from letsdns.configuration import Config


class Action(ABC):
    """Abstract base class for LetsDNS actions."""

    @abstractmethod
    def execute(self, conf: Config, *args, **kwargs):
        raise NotImplementedError  # pragma: no cover


def import_class(class_name: str):
    """Dynamically import a Python class. The containing module must be available in PYTHONPATH.

    Args:
        class_name: Fully qualified class name, e.g. "mymodule.submodule.MyClass".
    """
    # Split fully qualified name into components, the last being the class name.
    components = class_name.split('.')
    # Import the module containing the class.
    attribute = __import__('.'.join(components[:-1]))
    # Traverse the attribute hierarchy.
    for component in components[1:]:
        attribute = getattr(attribute, component)
    return attribute


def import_action(class_name: str) -> Type[Action]:
    """Dynamically import an action class. Raises a TypeError exception if the imported
    class is not a subclass of 'Action'.

    Args:
        class_name: Fully qualified class name, e.g. "mymodule.actions.SomeAction".
    """
    class_ = import_class(class_name)
    if issubclass(class_, Action):
        return class_
    raise TypeError(f'{class_} is no subclass of {Action}')
