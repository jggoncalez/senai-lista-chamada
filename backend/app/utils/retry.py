"""Função de retry para lidar com falhas temporárias em operações,
como chamadas de API ou acesso a banco de dados.

Ela tenta executar a função fornecida várias vezes, com um intervalo
crescente entre as tentativas, antes de desistir e lançar a última
exceção encontrada.
"""

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
            time.sleep(espera * (2 ** i))
