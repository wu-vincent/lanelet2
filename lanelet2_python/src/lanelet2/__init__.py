import os
from os.path import dirname
from pkgutil import iter_modules

if os.name == "nt":
    bin_dir = None

    try:
        bin_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bin"))
        try:
            os.add_dll_directory(bin_dir)
        except (Exception,):
            pass
        os.environ["PATH"] = bin_dir + ";" + os.environ["PATH"]
    except (Exception,):
        pass

    del bin_dir

# automatically import all files in this module
__all__ = [name for _, name, _ in iter_modules([dirname(__file__)])]

for module_name in __all__:
    from importlib import import_module

    module = import_module(__name__ + "." + module_name)
    if len(__all__) == 1:
        globals().update(module.__dict__)
    del module
