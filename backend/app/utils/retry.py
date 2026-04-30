import time
from typing import Callable, TypeVar

T = TypeVar("T")

def com_retry(fn: Callable[[], T], tentativas: int = 3, espera: float = 1.0) -> T:
    for i in range(tentativas):
        try:
            return fn()
        except Exception:
            if i == tentativas - 1:
                raise
            time.sleep(espera)
