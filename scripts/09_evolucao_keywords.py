#!/usr/bin/env python3
"""Incidencia de temas em keywords OpenAlex, janelas moveis de 5 anos.

Este grafico NAO estima topic models ou DTM. Mede exclusivamente a
ocorrencia de palavras-chave indexadas no nucleo provisorio do corpus.
"""
from pathlib import Path
import json
import csv
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
SOURCE = BASE / "resultados" / "triagem" / "05_nucleo_provisorio_openalex.json"
DEST = BASE / "resultados" / "analises"
DEST.mkdir(parents=True, exist_ok=True)

ALIASES = {
    "routine-biased technical change": "routine-biased technological change",
    "labour market polarization": "labor market polarization",
    "occupational polarisation": "occupational polarization",
    "job polarisation": "job polarization",
    "labour market": "labor market",
    "technological unemployment": "technology-induced unemployment",
}

TERMSETS = {
    "Rotinização / RBTC": {
        "routine-biased technological change", "routine tasks", "routine occupations"
    },
    "Automação": {"automation", "robotics", "industrial robots"},
    "Desigualdade salarial": {
        "wage inequality", "wage polarization", "wage distribution"
    },
    "Offshoring": {"offshoring"},
    "Inteligência artificial": {
        "artificial intelligence", "generative artificial intelligence",
        "generative ai", "machine learning", "ai technology"
    },
}

records = json.loads(SOURCE.read_text(encoding="utf-8"))["results"]
assert len(records) == 208, "Corpus alterado: conferir e atualizar a análise."
prepared = []
for record in records:
    terms = {
        ALIASES.get(k["display_name"].strip().lower(),
                    k["display_name"].strip().lower())
        for k in record.get("keywords", [])
        if k.get("display_name")
    }
    prepared.append({
        "ano": int(record["publication_year"]),
        **{name: int(bool(terms & words)) for name, words in TERMSETS.items()},
    })

rows = []
for end in range(2004, 2026):
    start = end - 4
    subset = [r for r in prepared if start <= r["ano"] <= end]
    if len(subset) < 20:
        continue
    for name in TERMSETS:
        count = sum(r[name] for r in subset)
        rows.append({
            "inicio": start,
            "fim": end,
            "tema": name,
            "n_artigos": len(subset),
            "artigos_com_termo": count,
            "percentual": 100 * count / len(subset),
        })

with (DEST / "evolucao_keywords_janelas_5anos.csv").open(
    "w", newline="", encoding="utf-8-sig"
) as output:
    writer = csv.DictWriter(output, fieldnames=rows[0].keys(), delimiter=";")
    writer.writeheader()
    writer.writerows(rows)

fig, ax = plt.subplots(figsize=(9.1, 4.4), dpi=170)
for name in TERMSETS:
    series = [r for r in rows if r["tema"] == name]
    ax.plot(
        [r["fim"] for r in series],
        [r["percentual"] for r in series],
        linewidth=2, marker="o", markersize=2.8, label=name,
    )
ax.set_title(
    "Mudança na incidência das palavras-chave (janelas de 5 anos)",
    fontsize=12.2, weight="bold", pad=11,
)
ax.set_xlabel("Último ano da janela móvel (5 anos)", fontsize=9.5)
ax.set_ylabel("Artigos com o tema (% da janela)", fontsize=9.5)
ax.set_xlim(min(r["fim"] for r in rows) - .35, 2025.35)
ax.set_ylim(bottom=0)
ax.set_xticks([2009, 2012, 2015, 2018, 2021, 2023, 2025])
ax.grid(axis="y", alpha=.20)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="upper right", frameon=False, fontsize=8.3, ncol=2)
fig.text(
    .5, .012,
    "Fonte: OpenAlex, núcleo provisório (n=208). Frequências observadas; "
    "não é um modelo dinâmico de tópicos.",
    ha="center", fontsize=8, color="#444444",
)
fig.subplots_adjust(bottom=.16, top=.87, left=.085, right=.98)
fig.savefig(
    DEST / "fig3_evolucao_janelas_5anos.png", dpi=210,
    bbox_inches="tight",
)
plt.close(fig)
print("Evolução temática gerada:", len(records), "artigos;", len(rows), "linhas.")
