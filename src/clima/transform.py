"""Leitura e limpeza dos arquivos GSOD da estação Curitiba–Afonso Pena."""

from __future__ import annotations

import math
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

AUSENTE_TEMPERATURA = 9999.9
COLUNAS_TEMPERATURA = {"TEMP": "temp_c", "MAX": "max_c", "MIN": "min_c"}


def f_para_c(valor_f: float) -> float:
    """Converte °F para °C; a sentinela 9999.9 vira NaN."""
    if valor_f == AUSENTE_TEMPERATURA:
        return math.nan
    return round((valor_f - 32) * 5 / 9, 2)


def pol_para_mm(valor_pol: float) -> float:
    """Converte precipitação de polegadas para milímetros."""
    return round(valor_pol * 25.4, 1)


def ler_gsod(arquivos: Iterable[Path]) -> pd.DataFrame:
    """Lê os CSV brutos e devolve uma linha por dia, em °C."""
    bruto = pd.concat(pd.read_csv(arquivo) for arquivo in sorted(arquivos))
    dias = pd.DataFrame({"data": pd.to_datetime(bruto["DATE"])})
    for origem, destino in COLUNAS_TEMPERATURA.items():
        dias[destino] = bruto[origem].astype(float).map(f_para_c).to_numpy()
    dias["chuva_mm"] = bruto["PRCP"].astype(float).map(pol_para_mm).to_numpy()
    return dias.sort_values("data").reset_index(drop=True)


def resumo_mensal(dias: pd.DataFrame) -> pd.DataFrame:
    """Resume a série diária por mês, registrando quantos dias têm dado."""
    mes = dias["data"].dt.to_period("M")
    resumo = dias.groupby(mes).agg(
        dias_com_dado=("temp_c", "count"),
        temp_media=("temp_c", "mean"),
        max_media=("max_c", "mean"),
        min_media=("min_c", "mean"),
        chuva_total=("chuva_mm", "sum"),
        dias_com_chuva_medida=("chuva_mm", "count"),
    )
    resumo.index.name = "mes"
    resumo["dias_no_mes"] = resumo.index.days_in_month
    resumo["cobertura"] = resumo["dias_com_dado"] / resumo["dias_no_mes"]
    return resumo.round(2)


def anomalia(resumo: pd.DataFrame, mes: str, referencia: tuple[int, int]) -> float:
    """Diferença entre a temperatura média do mês e a média do mesmo mês no período."""
    alvo = pd.Period(mes, freq="M")
    inicio, fim = referencia
    mesmo_mes = resumo[
        (resumo.index.month == alvo.month)
        & (resumo.index.year >= inicio)
        & (resumo.index.year <= fim)
    ]
    return round(resumo.loc[alvo, "temp_media"] - mesmo_mes["temp_media"].mean(), 2)
