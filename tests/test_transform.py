import math

from clima.transform import f_para_c


def test_temperatura_media_de_1_jan_2024():
    # data/raw/gsod_83842_2024.csv, 2024-01-01: TEMP = 70.6 °F
    assert f_para_c(70.6) == 21.44


def test_minima_ausente_em_17_dez_2020_vira_nan():
    # data/raw/gsod_83842_2020.csv, 2020-12-17: MIN = 9999.9 (sem leitura)
    assert math.isnan(f_para_c(9999.9))
