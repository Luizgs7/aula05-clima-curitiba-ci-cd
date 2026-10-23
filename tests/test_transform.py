import math
from pathlib import Path

import pytest

from clima.transform import anomalia, f_para_c, ler_gsod, resumo_mensal

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"


def test_temperatura_media_de_1_jan_2024():
    # data/raw/gsod_83842_2024.csv, 2024-01-01: TEMP = 70.6 °F
    assert f_para_c(70.6) == 21.44


def test_minima_ausente_em_17_dez_2020_vira_nan():
    # data/raw/gsod_83842_2020.csv, 2020-12-17: MIN = 9999.9 (sem leitura)
    assert math.isnan(f_para_c(9999.9))


@pytest.fixture(scope="module")
def dias():
    return ler_gsod(RAW.glob("gsod_83842_*.csv"))


def test_serie_vai_de_2015_ate_24_ago_2025(dias):
    assert str(dias["data"].min().date()) == "2015-01-01"
    assert str(dias["data"].max().date()) == "2025-08-24"


def test_outubro_2020_tem_so_6_dias(dias):
    resumo = resumo_mensal(dias)
    assert resumo.loc["2020-10", "dias_com_dado"] == 6
    assert resumo.loc["2020-10", "cobertura"] == pytest.approx(6 / 31, abs=0.01)


def test_anomalia_e_zero_quando_mes_e_o_proprio_periodo(dias):
    resumo = resumo_mensal(dias)
    assert anomalia(resumo, "2024-07", referencia=(2024, 2024)) == 0
