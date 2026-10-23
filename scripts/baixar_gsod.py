"""Baixa dados diários da estação Curitiba / Bacacheri (OMM 83842) no NOAA GSOD.

Uso:
    python scripts/baixar_gsod.py 2015 2026

Cada ano vira um arquivo em data/raw/gsod_83842_AAAA.csv, exatamente como a
API devolve (°F, polegadas e sentinelas como 9999.9). Toda limpeza acontece em
src/clima/transform.py, onde pode ser testada.
"""

from __future__ import annotations

import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ESTACAO = "83842099999"
API = "https://www.ncei.noaa.gov/access/services/data/v1"
DESTINO = Path(__file__).resolve().parents[1] / "data" / "raw"


def url_do_ano(ano: int) -> str:
    fim = min(date(ano, 12, 31), date.today())
    params = {
        "dataset": "global-summary-of-the-day",
        "stations": ESTACAO,
        "startDate": f"{ano}-01-01",
        "endDate": fim.isoformat(),
        "format": "csv",
    }
    return f"{API}?{urllib.parse.urlencode(params)}"


def baixar(ano: int) -> Path | None:
    url = url_do_ano(ano)
    with urllib.request.urlopen(url, timeout=120) as resposta:
        conteudo = resposta.read()
    destino = DESTINO / f"gsod_83842_{ano}.csv"
    linhas = conteudo.count(b"\n") - 1
    if linhas <= 0:
        print(f"{ano}: nenhum dia disponível na API; nada gravado")
        return None
    if destino.exists() and destino.read_bytes() == conteudo:
        print(f"{ano}: {linhas} dias, sem mudança em {destino.name}")
        return None
    destino.write_bytes(conteudo)
    print(f"{ano}: {linhas} dias -> {destino.name}")
    registrar_fonte(ano, url, linhas)
    return destino


def registrar_fonte(ano: int, url: str, linhas: int) -> None:
    fonte = DESTINO / "FONTE.md"
    agora = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with fonte.open("a", encoding="utf-8") as arquivo:
        arquivo.write(f"| {ano} | {linhas} | {agora} | <{url}> |\n")


def main(argv: list[str]) -> None:
    inicio, fim = int(argv[1]), int(argv[2])
    DESTINO.mkdir(parents=True, exist_ok=True)
    for ano in range(inicio, fim + 1):
        baixar(ano)


if __name__ == "__main__":
    main(sys.argv)
