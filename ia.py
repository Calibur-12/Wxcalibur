import json
import os
import re
import ollama


ARQUIVO_MEMORIA = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "memoria.json"
)

PASTA_CONHECIMENTO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "conhecimento"
)

MODELO = "qwen3:1.7b"

MAX_RESULTADOS_CONHECIMENTO = 3
MAX_RESULTADOS_MEMORIA = 2


def carregar_memoria():

    if not os.path.exists(ARQUIVO_MEMORIA):
        return {}

    try:

        with open(
            ARQUIVO_MEMORIA,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)

    except:

        return {}


def salvar_memoria(memoria):

    with open(
        ARQUIVO_MEMORIA,
        "w",
        encoding="utf-8"
    ) as arquivo:

        json.dump(
            memoria,
            arquivo,
            indent=4,
            ensure_ascii=False
        )


def carregar_conhecimento():

    conhecimento = []

    if not os.path.exists(PASTA_CONHECIMENTO):
        return conhecimento

    for arquivo in os.listdir(PASTA_CONHECIMENTO):

        if not arquivo.endswith(".json"):
            continue

        caminho = os.path.join(
            PASTA_CONHECIMENTO,
            arquivo
        )

        try:

            with open(
                caminho,
                "r",
                encoding="utf-8"
            ) as f:

                dados = json.load(f)

            if isinstance(dados, list):

                conhecimento.extend(dados)

        except Exception as erro:

            print(
                f"Erro ao carregar {arquivo}: {erro}"
            )

    return conhecimento


def palavras(texto):

    texto = texto.lower()

    return set(
        re.findall(
            r"\b\w+\b",
            texto
        )
    )


def buscar_conhecimento(
    pergunta,
    conhecimento
):

    palavras_pergunta = palavras(
        pergunta
    )

    resultados = []

    for item in conhecimento:

        texto = (
            item.get("pergunta", "")
            + " "
            + item.get("resposta", "")
        )

        palavras_item = palavras(
            texto
        )

        pontos = len(
            palavras_pergunta
            & palavras_item
        )

        if pontos > 0:

            resultados.append(
                (pontos, item)
            )

    resultados.sort(
        key=lambda resultado: resultado[0],
        reverse=True
    )

    return [
        item
        for pontos, item
        in resultados[
            :MAX_RESULTADOS_CONHECIMENTO
        ]
    ]


def buscar_memoria(
    pergunta,
    memoria
):

    palavras_pergunta = palavras(
        pergunta
    )

    resultados = []

    for chave, valor in memoria.items():

        texto = (
            chave
            + " "
            + str(valor)
        )

        palavras_memoria = palavras(
            texto
        )

        pontos = len(
            palavras_pergunta
            & palavras_memoria
        )

        if pontos > 0:

            resultados.append(
                (
                    pontos,
                    chave,
                    valor
                )
            )

    resultados.sort(
        key=lambda resultado: resultado[0],
        reverse=True
    )

    return resultados[
        :MAX_RESULTADOS_MEMORIA
    ]


def conversar(
    mensagem,
    memoria,
    historico,
    conhecimento
):

    memorias_relevantes = buscar_memoria(
        mensagem,
        memoria
    )

    memorias = ""

    for pontos, chave, valor in memorias_relevantes:

        memorias += (
            f"- {chave}: {valor}\n"
        )

    if not memorias:

        memorias = (
            "Nenhuma memória relevante."
        )


    conhecimentos_relevantes = (
        buscar_conhecimento(
            mensagem,
            conhecimento
        )
    )

    informacoes = ""

    for item in conhecimentos_relevantes:

        pergunta = item.get(
            "pergunta",
            ""
        )

        resposta = item.get(
            "resposta",
            ""
        )

        informacoes += (
            f"Pergunta: {pergunta}\n"
            f"Resposta: {resposta}\n\n"
        )

    if not informacoes:

        informacoes = (
            "Nenhuma informação "
            "relevante encontrada."
        )


    mensagens = [

        {
            "role": "system",

            "content": f"""
Você é a Wxcalibur 0.2.

Você é uma inteligência artificial
local criada em Python no Brasil.

Responda em português quando o usuário
falar português.

Seja amigável, direto e simples.

Use as informações relevantes abaixo
quando elas ajudarem na resposta.

Não invente informações presentes na
memória ou na base de conhecimento.

MEMÓRIAS RELEVANTES:
{memorias}

CONHECIMENTO RELEVANTE:
{informacoes}
"""
        }

    ]


    mensagens.extend(
        historico
    )


    mensagens.append({

        "role": "user",

        "content": mensagem

    })


    resposta = ollama.chat(

        model=MODELO,

        messages=mensagens

    )


    texto = resposta[
        "message"
    ][
        "content"
    ]


    texto = texto.replace(
        "**",
        ""
    )

    texto = texto.replace(
        "__",
        ""
    )


    return texto


def aprender(
    chave,
    valor,
    memoria
):

    chave = chave.strip().lower()

    valor = valor.strip()

    memoria[chave] = valor

    salvar_memoria(
        memoria
    )

    return (
        f"Aprendi! 🧠 "
        f"{chave} = {valor}"
    )


def lembrar(
    chave,
    memoria
):

    chave = chave.strip().lower()

    if chave in memoria:

        return (
            f"Eu lembro! 🧠 "
            f"{chave} = "
            f"{memoria[chave]}"
        )

    return (
        f"Não lembro de "
        f"'{chave}' ainda."
    )