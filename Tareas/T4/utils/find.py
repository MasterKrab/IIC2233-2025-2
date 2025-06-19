from typing import Callable, Iterable, TypeVar


T = TypeVar("T")


def find(function: Callable[[T], bool], items: Iterable[T]) -> T | None:
    for item in items:
        if function(item):
            return item

    return None
