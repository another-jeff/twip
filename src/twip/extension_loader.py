# src/twip/extension_loader.py

from importlib import import_module
from types import ModuleType


Extension = ModuleType | str


def load_extension(extension: Extension) -> ModuleType:
    module = _import_extension(extension)
    register = getattr(module, "register", None)

    if register is None:
        raise ValueError(f"Extension module has no register(): {module.__name__}")

    if not callable(register):
        raise TypeError(f"Extension register is not callable: {module.__name__}")

    register()
    return module


def _import_extension(extension: Extension) -> ModuleType:
    if isinstance(extension, str):
        return import_module(extension)

    return extension