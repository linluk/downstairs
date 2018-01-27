
import sys
import inspect
from typing import Callable, Iterator, Type

def classes_from_module(module_name: str, predicate: Callable[[Type], bool] = None) -> Iterator:
  """ https://stackoverflow.com/a/46206754/3403216 """
  if predicate is None:
    predicate = lambda _: True
  if module_name in sys.modules:
    for _, cls in inspect.getmembers(sys.modules[module_name],
                                     lambda o: inspect.isclass(o) and o.__module__ == module_name):
      if predicate(cls):
        yield cls

