"""Leitura e limpeza dos arquivos GSOD da estação Curitiba–Afonso Pena."""

from __future__ import annotations

import math

AUSENTE_TEMPERATURA = 9999.9


def f_para_c(valor_f: float) -> float:
    """Converte °F para °C; a sentinela 9999.9 vira NaN."""
    if valor_f == AUSENTE_TEMPERATURA:
        return math.nan
    return round((valor_f - 32) * 5 / 9, 2)
