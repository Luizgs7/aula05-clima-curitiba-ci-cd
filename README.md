# Clima de Curitiba — relatório reproduzível

Repositório de exemplo da **Aula 05 (Git, CI/CD e automação de relatórios)** da
Especialização em Inteligência Artificial Generativa — Departamento de Estatística, UFPR.

O relatório resume temperatura e chuva diárias da estação **Curitiba / Afonso Pena
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

## Rodar localmente

```bash
python -m pip install -r requirements.txt
ruff check src tests scripts
python -m pytest
quarto render report.qmd
```

## Laboratório

Faça um *fork*, ative o GitHub Actions no fork e siga as instruções da aula.
As pull requests fechadas deste repositório mostram falhas reais de CI — provocadas de
propósito para a aula — e as correções correspondentes.
