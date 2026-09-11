import json
import os
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


def conversar(
    mensagem,
    memoria,
    historico,
    conhecimento
):

    memorias = ""

    if memoria:

        for chave, valor in memoria.items():

            memorias += (
                f"- {chave}: {valor}\n"
            )

    else:

        memorias = "Nenhuma memória."


    informacoes = ""

    for item in conhecimento:

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


    mensagens = [

        {
            "role": "system",

            "content": f"""
Você é a Wxcalibur 0.3.

Você é uma inteligência artificial
local criada em Python.

Responda em português quando o usuário
falar português.

Seja amigável e explique as coisas
de maneira simples.

Você possui uma base de conhecimento.

Use o conhecimento abaixo quando ele
for útil para responder.

MEMÓRIAS:
{memorias}

CONHECIMENTO:
{informacoes}
"""
        }

    ]


    mensagens.extend(historico)


    mensagens.append({

        "role": "user",

        "content": mensagem

    })


    resposta = ollama.chat(

        model=MODELO,

        messages=mensagens

    )


    texto = resposta["message"]["content"]


    # Remove negrito Markdown
    texto = texto.replace("**", "")

    # Remove sublinhado Markdown
    texto = texto.replace("__", "")


    return texto


def aprender(
    chave,
    valor,
    memoria
):

    chave = chave.strip().lower()

    valor = valor.strip()

    memoria[chave] = valor

    salvar_memoria(memoria)

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

