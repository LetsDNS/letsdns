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
from logging import debug
from logging import warning
from typing import Type

from letsdns.configuration import Config


class Action(ABC):
    """Abstract base class for LetsDNS actions."""

    def pre_execute(self, conf: Config) -> int:
        """Pre-execution phase, for initialisation."""
        debug(f'{self}.pre_execute({conf})')
        return 0

    @abstractmethod
    def execute(self, conf: Config, *args, **kwargs) -> int:
        """Action classes MUST implement this method.

        All unknown positional and keyword arguments unknown to the implementing
        class MUST be ignored.

        Args:
            conf: Configuration data.
            args: Positional arguments.
            kwargs: Keyword arguments.
        """
        raise NotImplementedError  # pragma: no cover

    def post_execute(self, conf: Config) -> int:
        """Post-execution phase, for cleanup."""
        debug(f'{self}.post_execute({conf})')
        return 0


def _report(action, method: str, code: int):
    """Report the return code for an action's method.

    Args:
        action: Instance object of an 'Action' class.
        method: Method name.
        code: Code to report.
    """
    warning(f'{action.__class__.__name__}.{method} returned code {code}')


def dynamic_action(conf: Config, action: Action) -> int:
    """Invoke the lifecycle methods of a dynamically imported action. The first non-zero
    method return code will abort execution and will be returned to the caller.

    Args:
        conf: Configuration data.
        action: Instance object of an 'Action' class.
    """
    rc = action.pre_execute(conf)
    if rc == 0:
        rc = action.execute(conf)
        if rc == 0:
            rc = action.post_execute(conf)
            if rc != 0:
                _report(action, 'post_execute', rc)
        else:
            _report(action, 'execute', rc)
    else:
        _report(action, 'pre_execute', rc)
    return rc


def import_class(class_name: str):
    """Dynamically import a Python class. The containing module must be available in PYTHONPATH.

    Args:
        class_name: Fully qualified class name, e.g. "mymodule.submodule.MyClass".
    """
    debug(f'Import {class_name}')
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
