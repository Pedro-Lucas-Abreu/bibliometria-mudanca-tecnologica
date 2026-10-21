#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpenAlex — seis buscas da literatura de polarizacao ocupacional.

Objetivo: descarregar 6 consultas ja definidas na interface do OpenAlex,
registrar proveniencia, deduplicar por OpenAlex ID e gerar auditoria humana.
Usa exclusivamente bibliotecas da instalacao padrao do Python 3.10+.

COMO EXECUTAR:
  python openalex_unificar_validar.py
  python openalex_unificar_validar.py --teste-local

Autenticacao: OPENALEX_API_KEY no ambiente OU prompt oculto no terminal.
Nunca coloque sua chave de API diretamente neste arquivo.
"""

import argparse
import collections
import csv
import datetime as dt
import getpass
import itertools
import json
import os
from pathlib import Path
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

CONSULTAS = [
    ("B1", "job polarization", 1240),
    ("B2", "employment polarization", 1519),
    ("B3", "occupational polarization", 359),
    ("B4", "labor market polarization", 945),
    ("B5", "routine-biased technological change", 326),
    ("B6", "routine-biased technical change", 586),
]
ANO_INICIAL, ANO_FINAL = 2000, 2025
FILTROS = f"publication_year:{ANO_INICIAL}-{ANO_FINAL},type:article"
CAMPOS = [
    "id", "doi", "display_name", "publication_year", "publication_date",
    "type", "cited_by_count", "authorships", "primary_location",
    "keywords", "referenced_works", "abstract_inverted_index", "primary_topic",
    "language",
]
QUANTIDADE_PAGINA = 100
VERSAO_SCRIPT = "1.0"


def escrever_csv(caminho, colunas, linhas):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8-sig", newline="") as arquivo:
        w = csv.DictWriter(arquivo, fieldnames=colunas, delimiter=";", extrasaction="ignore")
        w.writeheader()
        for linha in linhas:
            w.writerow(linha)


def escrever_json(caminho, objeto):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    temporario = caminho.with_suffix(caminho.suffix + ".tmp")
    with temporario.open("w", encoding="utf-8") as arquivo:
        json.dump(objeto, arquivo, ensure_ascii=False, separators=(",", ":"))
    temporario.replace(caminho)


def ler_json(caminho):
    with caminho.open(encoding="utf-8") as arquivo:
        return json.load(arquivo)


def obter_api_key():
    chave = os.environ.get("OPENALEX_API_KEY", "").strip()
    if chave:
        return chave
    try:
        chave = getpass.getpass("Cole sua API key OpenAlex (entrada oculta): ").strip()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit("Para rodar sem prompt, defina OPENALEX_API_KEY no terminal.")
    if not chave:
        raise SystemExit("Chave vazia: obtenha gratuitamente em https://openalex.org/settings/api")
    return chave


def requisicao_openalex(parametros, api_key):
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(parametros)
    # O token no header nao fica visivel no URL ou no log de erros.
    headers = {
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "Pesquisa-academica-bibliometria/1.0",
        "Accept": "application/json",
    }
    for tentativa in range(6):
        try:
            with urllib.request.urlopen(
                urllib.request.Request(url, headers=headers), timeout=75
            ) as resposta:
                return json.load(resposta)
        except urllib.error.HTTPError as erro:
            if erro.code in (401, 403):
                raise RuntimeError(
                    "OpenAlex recusou a chave ou a cota diaria acabou (HTTP "
                    + str(erro.code) + "). Confira sua conta e o orcamento da API."
                ) from None
            if erro.code == 400:
                corpo = erro.read(1500).decode("utf-8", errors="replace")
                raise RuntimeError("Consulta rejeitada pelo OpenAlex: " + corpo) from None
            if erro.code not in (429, 500, 502, 503, 504):
                raise
            espera = min(2 ** tentativa * 3, 60)
            print(f"  HTTP {erro.code}: aguardando {espera}s para tentar novamente.")
        except (TimeoutError, urllib.error.URLError) as erro:
            espera = min(2 ** tentativa * 3, 60)
            print(f"  Falha de rede: {erro}. Aguardando {espera}s.")
        if tentativa < 5:
            time.sleep(espera)
    raise RuntimeError("Nao foi possivel concluir a requisicao apos seis tentativas.")


def baixar_consulta(codigo, frase, api_key, pasta_cache):
    # Cada pagina fica armazenada em disco. Em interrupcao, a execucao seguinte
    # reusa as paginas existentes e continua pelo cursor salvo na ultima pagina.
    pasta = pasta_cache / codigo
    pasta.mkdir(parents=True, exist_ok=True)
    cursor = "*"
    proxima_pagina = 1
    ids_na_consulta = set()
    trabalhos = []
    esperado_api = None
    vistos_cursores = set()

    while cursor:
        if cursor in vistos_cursores:
            raise RuntimeError(f"Cursor repetido na busca {codigo}, evitando loop infinito.")
        vistos_cursores.add(cursor)
        arq_pagina = pasta / f"pagina_{proxima_pagina:04d}.json"
        if arq_pagina.exists():
            dados = ler_json(arq_pagina)
            origem = "cache"
        else:
            parametros = {
                "search.title_abstract_keywords": frase,
                "filter": FILTROS,
                "sort": "relevance_score:desc",
                "per_page": QUANTIDADE_PAGINA,
                "cursor": cursor,
                "select": ",".join(CAMPOS),
            }
            dados = requisicao_openalex(parametros, api_key)
            escrever_json(arq_pagina, dados)
            origem = "API"
            time.sleep(0.12)
        meta = dados.get("meta", {}) or {}
        if esperado_api is None:
            esperado_api = meta.get("count")
        resultado = dados.get("results", []) or []
        for trabalho in resultado:
            id_ = trabalho.get("id")
            if not id_:
                raise RuntimeError("Trabalho sem ID OpenAlex encontrado.")
            if id_ in ids_na_consulta:
                continue
            ids_na_consulta.add(id_)
            trabalhos.append(trabalho)
        proximo_cursor = meta.get("next_cursor")
        print(f"  {codigo} pagina {proxima_pagina:03d} [{origem}]: "
              f"{len(trabalhos)} / {esperado_api if esperado_api is not None else '?'}")
        if not resultado or not proximo_cursor:
            break
        cursor = proximo_cursor
        proxima_pagina += 1
        if proxima_pagina > 300:
            raise RuntimeError("Mais de 300 paginas: verifique sua consulta.")
    return trabalhos, esperado_api


def reconstituir_resumo(inv):
    if not isinstance(inv, dict) or not inv:
        return ""
    indices = [i for posicoes in inv.values() for i in posicoes if isinstance(i, int)]
    if not indices:
        return ""
    tokens = [""] * (max(indices) + 1)
    for palavra, posicoes in inv.items():
        for posicao in posicoes:
            if isinstance(posicao, int) and 0 <= posicao < len(tokens):
                tokens[posicao] = palavra
    return " ".join(tokens).strip()


def nome_artigo(artigo):
    return artigo.get("display_name") or artigo.get("title") or ""


def atributo_linha(artigo, codigos):
    autores = [
        (a.get("author") or {}).get("display_name", "")
        for a in artigo.get("authorships") or []
    ]
    paises = sorted({
        cod
        for a in artigo.get("authorships") or []
        for cod in (a.get("countries") or [])
        if cod
    })
    instituicoes = sorted({
        i.get("display_name")
        for a in artigo.get("authorships") or []
        for i in (a.get("institutions") or [])
        if i.get("display_name")
    })
    revista = ((artigo.get("primary_location") or {}).get("source") or {}).get("display_name", "")
    topico = artigo.get("primary_topic") or {}
    palavras = [kw.get("display_name", "") for kw in artigo.get("keywords") or []]
    resumo = reconstituir_resumo(artigo.get("abstract_inverted_index"))
    return {
        "openalex_id": artigo.get("id", ""),
        "doi": artigo.get("doi") or "",
        "titulo": nome_artigo(artigo),
        "ano": artigo.get("publication_year") or "",
        "data_publicacao": artigo.get("publication_date") or "",
        "tipo": artigo.get("type") or "",
        "citacoes": artigo.get("cited_by_count") or 0,
        "autores": " | ".join(a for a in autores if a),
        "paises": " | ".join(paises),
        "instituicoes": " | ".join(instituicoes),
        "periodico": revista,
        "topico_primario": topico.get("display_name", ""),
        "area_topico": (topico.get("field") or {}).get("display_name", ""),
        "idioma": artigo.get("language") or "",
        "palavras_openalex": " | ".join(p for p in palavras if p),
        "resumo": resumo,
        "n_referencias": len(artigo.get("referenced_works") or []),
        "n_buscas": len(codigos),
        "buscas": " | ".join(sorted(codigos)),
    }


def sinalizar_revisao(linha):
    # Isso NAO exclui artigo. So prioriza a leitura humana de textos suspeitos.
    titulo = linha["titulo"].lower()
    resumo = linha["resumo"].lower()
    texto = titulo + " " + resumo
    termos_politicos = [
        "political polarization", "affective polarization", "electoral polarization",
        "partisan polarization", "political parties", "partisanship", "electoral behavior",
    ]
    termos_relevantes = [
        "employment", "labour", "labor", "occupation", "technolog", "automat",
        "routine", "wage", "skill", "job", "income inequality", "task",
    ]
    if any(t in titulo for t in termos_politicos):
        return "REVISAR_POLITICA"
    if not any(t in texto for t in termos_relevantes):
        return "REVISAR_SEM_INDICADOR_LABORAL"
    return "SEM_ALERTA_AUTOMATICO"


def gerar_saida(resultado_por_busca, contagens_api, destino, origem="api"):
    destino.mkdir(parents=True, exist_ok=True)
    trabalhos_por_id = {}
    presenca = collections.defaultdict(set)
    freq_doc = collections.Counter()
    for codigo, frase, contagem_manual in CONSULTAS:
        trabalhos = resultado_por_busca[codigo]
        for trabalho in trabalhos:
            id_ = trabalho["id"]
            if id_ not in trabalhos_por_id:
                trabalhos_por_id[id_] = trabalho
            presenca[id_].add(codigo)
        freq_doc[codigo] = len({w["id"] for w in trabalhos})

    linhas = [atributo_linha(w, presenca[id_])
              for id_, w in sorted(trabalhos_por_id.items())]
    linhas.sort(key=lambda x: (-(int(x["citacoes"])), x["openalex_id"]))
    colunas = list(linhas[0]) if linhas else []
    if not colunas:
        raise RuntimeError("Nenhum registro encontrado: nao ha base para exportar.")
    escrever_csv(destino / "01_base_unificada.csv", colunas, linhas)

    resumo = []
    for codigo, frase, contagem_manual in CONSULTAS:
        dif = (contagens_api[codigo] - contagem_manual
               if contagens_api[codigo] is not None else "")
        resumo.append({
            "busca": codigo, "expressao": frase,
            "contagem_site_anotada": contagem_manual,
            "contagem_api_atual": contagens_api[codigo],
            "IDs_baixados_unicos_na_consulta": freq_doc[codigo],
            "diferenca_api_vs_site": dif,
        })
    escrever_csv(destino / "02_auditoria_buscas.csv", list(resumo[0]), resumo)

    sobreposicoes = []
    for (a, _, _), (b, _, _) in itertools.product(CONSULTAS, repeat=2):
        A = {id_ for id_, bs in presenca.items() if a in bs}
        B = {id_ for id_, bs in presenca.items() if b in bs}
        sobreposicoes.append({
            "busca_1": a, "busca_2": b, "intersecao": len(A & B),
            "uniao": len(A | B), "jaccard": round(len(A & B) / len(A | B), 5) if A | B else 0,
        })
    escrever_csv(destino / "03_sobreposicao_buscas.csv", list(sobreposicoes[0]), sobreposicoes)

    serie = collections.Counter(int(l["ano"]) for l in linhas if str(l["ano"]).isdigit())
    escrever_csv(destino / "04_producao_anual.csv", ["ano", "n_artigos"], [
        {"ano": ano, "n_artigos": serie.get(ano, 0)}
        for ano in range(ANO_INICIAL, ANO_FINAL + 1)
    ])

    freq_keywords = collections.Counter()
    for w in trabalhos_por_id.values():
        kw_por_trabalho = {k.get("display_name", "").strip() for k in w.get("keywords") or []}
        freq_keywords.update(k for k in kw_por_trabalho if k)
    escrever_csv(destino / "05_frequencia_keywords.csv", ["palavra_chave", "n_artigos"], [
        {"palavra_chave": p, "n_artigos": n}
        for p, n in sorted(freq_keywords.items(), key=lambda x: (-x[1], x[0]))
    ])

    # Amostra fixa: ate 40 sorteados, ate 20 mais citados e ate 20 alertas automatizados.
    gerador = random.Random(20261010)
    sorteados = gerador.sample(linhas, min(40, len(linhas)))
    mais_citados = sorted(linhas, key=lambda x: int(x["citacoes"]), reverse=True)[:20]
    suspeitos = [l for l in linhas if sinalizar_revisao(l) != "SEM_ALERTA_AUTOMATICO"]
    suspeitos = gerador.sample(suspeitos, min(20, len(suspeitos)))
    amostra = collections.OrderedDict()
    for grupo, seq in [("ALEATORIO", sorteados), ("MAIS_CITADOS", mais_citados),
                       ("ALERTA_TEMATICO", suspeitos)]:
        for l in seq:
            id_ = l["openalex_id"]
            if id_ not in amostra:
                registro = dict(l)
                registro["origem_amostra"] = grupo
                registro["alerta_automatico"] = sinalizar_revisao(l)
                registro["decisao_manual"] = ""  # preencher com INCLUIR ou EXCLUIR
                registro["motivo_decisao"] = ""
                amostra[id_] = registro
    escrever_csv(destino / "06_amostra_para_validar.csv",
                 colunas + ["origem_amostra", "alerta_automatico", "decisao_manual", "motivo_decisao"],
                 amostra.values())

    # Formato de resultado OpenAlex: pode ser selecionado em JSON File (optional)
    # no assistente de importacao OpenAlex do VOSviewer, sujeito a compatibilidade de versao.
    bruto = {
        "meta": {"count": len(trabalhos_por_id), "per_page": len(trabalhos_por_id),
                 "source": "six deduplicated OpenAlex search results"},
        "results": [trabalhos_por_id[id_] for id_ in sorted(trabalhos_por_id)],
        "group_by": [],
    }
    escrever_json(destino / "07_openalex_uniao_vosviewer.json", bruto)

    manifesto = {
        "coleta_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "versao_script": VERSAO_SCRIPT,
        "origem": origem,
        "endpoint": "https://api.openalex.org/works",
        "campo_de_busca": "search.title_abstract_keywords",
        "filtros": FILTROS,
        "tipo": "article",
        "anos": [ANO_INICIAL, ANO_FINAL],
        "sort": "relevance_score:desc",
        "per_page": QUANTIDADE_PAGINA,
        "campos": CAMPOS,
        "consultas": [dict(codigo=c, frase=f, contagem_site_anotada=n) for c, f, n in CONSULTAS],
        "n_unicos": len(trabalhos_por_id),
        "n_somados_consultas_api": sum(freq_doc.values()),
        "seed_amostra": 20261010,
        "nota": "Nenhuma exclusao automatica por conteudo foi aplicada; auditar manualmente.",
    }
    escrever_json(destino / "08_manifesto_metodo.json", manifesto)

    n_total = sum(freq_doc.values())
    n_unicos = len(trabalhos_por_id)
    alerta = collections.Counter(sinalizar_revisao(l) for l in linhas)
    linhas_relatorio = [
        "AUDITORIA DA BASE — OPENALEX", "=" * 65,
        "Data UTC: " + manifesto["coleta_utc"],
        f"Registros somados nas seis buscas da API: {n_total}",
        f"Artigos unicos (OpenAlex ID): {n_unicos}",
        f"Sobreposicoes removidas: {n_total-n_unicos}",
        f"Tamanho da amostra de validacao: {len(amostra)}",
        f"Suspeitas para revisao (na base inteira): {dict(alerta)}",
        "", "DIFERENCAS DE CONTAGEM COM O SITE:",
    ]
    for r in resumo:
        linhas_relatorio.append(
            f"  {r['busca']} {r['expressao']}: site {r['contagem_site_anotada']}, "
            f"API {r['contagem_api_atual']}, baixados {r['IDs_baixados_unicos_na_consulta']}"
        )
    linhas_relatorio += [
        "", "INTERPRETACAO:",
        "1. O numero de buscas NAO corresponde ao numero de artigos unicos.",
        "2. Uma busca no OpenAlex pode captar registros pelo texto OU keywords automaticas.",
        "3. O arquivo 06 requer auditoria humana de titulo e resumo; nao e filtro definitivo.",
        "4. O teste de pertinencia deve distinguir polarizacao ocupacional de politica.",
        "5. Conclusoes de rede dependem da estrategia de busca e da indexacao OpenAlex.",
        "6. O campo palavras_openalex pode conter keywords atribuidas automaticamente.",
        "7. Para VOSviewer: usar a opcao OpenAlex -> JSON File (optional),"
        "   apontando para 07_openalex_uniao_vosviewer.json, se a versao aceitar.",
        "8. Guarde cache e manifesto para reprodutibilidade.",
    ]
    (destino / "09_relatorio_qualidade.txt").write_text(
        "\n".join(linhas_relatorio) + "\n", encoding="utf-8"
    )
    print("\n" + "\n".join(linhas_relatorio[:7]))
    print(f"Arquivos gerados em: {destino.resolve()}")
    return n_unicos


def demo_offline():
    ids_por_busca = {
        "B1": ["W1", "W2", "W3"], "B2": ["W2", "W4", "W5"],
        "B3": ["W3", "W5"], "B4": ["W4", "W5"],
        "B5": ["W6"], "B6": ["W2", "W6"],
    }
    banco = {}
    for n in range(1, 7):
        id_ = f"https://openalex.org/W{n}"
        banco[f"W{n}"] = {
            "id": id_, "doi": None,
            "display_name": ["", "Routine employment and skills", "Political polarization",
                             "Occupational polarization study", "Artificial intelligence and work",
                             "Employment and jobs", "Routine-biased technological change"][n],
            "publication_year": 2000+n, "type": "article",
            "cited_by_count": 100*n,
            "authorships": [{"author": {"display_name": "Author " + str(n)},
                            "countries": ["BR"], "institutions": []}],
            "primary_location": {"source": {"display_name": "Economic Journal"}},
            "keywords": [{"display_name": "employment"}],
            "referenced_works": [], "abstract_inverted_index": {"employment": [0], "research": [1]},
            "primary_topic": {"display_name": "Labour economics", "field": {"display_name": "Economics"}},
        }
    resultados = {
        codigo: [banco[id_curto] for id_curto in ids]
        for codigo, ids in ids_por_busca.items()
    }
    contagens = {codigo: len(resultados[codigo]) for codigo, _, _ in CONSULTAS}
    import tempfile
    with tempfile.TemporaryDirectory(prefix="openalex_teste_") as t:
        alvo = Path(t) / "saidas"
        n = gerar_saida(resultados, contagens, alvo, origem="SIMULACAO_LOCAL")
        assert n == 6, n
        with (alvo / "01_base_unificada.csv").open(encoding="utf-8-sig") as a:
            linhas = list(csv.DictReader(a, delimiter=";"))
        assert len(linhas) == 6
        for nome in ["02_auditoria_buscas.csv", "03_sobreposicao_buscas.csv",
                     "04_producao_anual.csv", "05_frequencia_keywords.csv",
                     "06_amostra_para_validar.csv", "07_openalex_uniao_vosviewer.json",
                     "08_manifesto_metodo.json", "09_relatorio_qualidade.txt"]:
            assert (alvo / nome).exists(), nome
        texto = (alvo / "09_relatorio_qualidade.txt").read_text(encoding="utf-8")
        assert "Sobreposicoes removidas: 7" in texto, texto
        print("TESTE LOCAL APROVADO: deduplicacao, CSV, amostra, manifesto e JSON.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--teste-local", action="store_true",
                        help="Testa a logica com dados simulados; nao consulta a API.")
    args = parser.parse_args()
    if args.teste_local:
        demo_offline()
        return
    # Roda corretamente em artigo/.../dados/scripts/, sem depender do CWD.
    pasta_script = Path(__file__).resolve().parent
    if pasta_script.name.lower() == "scripts" and pasta_script.parent.name.lower() == "dados":
        pasta_dados = pasta_script.parent
    else:
        pasta_dados = pasta_script
    destino = pasta_dados / "resultados_openalex"
    cache = destino / "cache_paginas"
    destino.mkdir(parents=True, exist_ok=True)

    print("OpenAlex: 6 consultas, busca em titulo/resumo/keywords, artigos 2000–2025")
    print("Arquivos de cache evitam baixar paginas ja obtidas.")
    print("A chave sera lida de forma oculta; nao fica salva nos arquivos.")
    key = obter_api_key()
    resultados = {}
    contagens = {}
    for codigo, frase, _ in CONSULTAS:
        print(f"\n[{codigo}] {frase}")
        resultados[codigo], contagens[codigo] = baixar_consulta(codigo, frase, key, cache)
    gerar_saida(resultados, contagens, destino)


if __name__ == "__main__":
    main()
