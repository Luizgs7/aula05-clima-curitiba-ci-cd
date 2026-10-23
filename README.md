# Clima de Curitiba — relatório reproduzível

Repositório de exemplo da **Aula 05 (Git, CI/CD e automação de relatórios)** da
Especialização em Inteligência Artificial Generativa — Departamento de Estatística, UFPR.

O relatório resume temperatura e chuva diárias da estação **Curitiba / Bacacheri
(OMM 83842)** a partir do NOAA GSOD. Os dados são reais: chegam em °F e polegadas, com
valores ausentes codificados como `9999.9` e `99.99`. Veja [`data/raw/FONTE.md`](data/raw/FONTE.md).

| Pasta / arquivo | Papel |
|---|---|
| `scripts/baixar_gsod.py` | Baixa os dados brutos da API da NOAA |
| `data/raw/` | Arquivos brutos, exatamente como a API entrega |
| `src/clima/` | Limpeza e resumos (código testável) |
| `tests/` | Testes com linhas reais dos arquivos |
| `report.qmd` | Relatório Quarto |
| `.github/workflows/` | Qualidade, renderização, publicação e atualização dos dados |

## Siglas

| Sigla | Significado |
|---|---|
| NOAA | *National Oceanic and Atmospheric Administration* — agência dos EUA para oceanos e atmosfera |
| NCEI | *National Centers for Environmental Information* — setor da NOAA que arquiva e distribui os dados |
| GSOD | *Global Summary of the Day* — resumo diário de milhares de estações meteorológicas do mundo |
| OMM | Organização Meteorológica Mundial (em inglês, WMO) — atribui o código de estação 83842 |
| ICAO | *International Civil Aviation Organization* — código de aeroporto (SBBI = Bacacheri) |
| INMET | Instituto Nacional de Meteorologia — órgão oficial de meteorologia do Brasil |
| FRSHTT | *Fog, Rain, Snow, Hail, Thunder, Tornado* — seis indicadores (0/1) do que ocorreu no dia |
| UTC | Tempo Universal Coordenado — referência de horário do cron do GitHub Actions |

## Rodar localmente

```bash
python -m pip install -r requirements.txt
ruff check src tests scripts
python -m pytest
quarto render report.qmd
```

## Laboratório

Faça um *fork*, ative o GitHub Actions na aba **Actions** do fork (em forks ele vem desativado)
e siga as instruções da aula. Em repositórios públicos, os runners hospedados do GitHub são gratuitos.

As pull requests #1 a #7 mostram falhas reais — provocadas de propósito para a aula —
e as correções correspondentes. A #8 corrige um erro real, não provocado: o nome da estação. **Neste repositório o GitHub Actions está desativado**, então as PRs
não exibem checks e o relatório não está publicado no Pages; as saídas das falhas estão nos
comentários das PRs e nos slides da aula. Num fork com Actions ativo, os quatro workflows rodam
como descrito.
