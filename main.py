from ia import (
    conversar,
    aprender,
    lembrar,
    carregar_memoria,
    carregar_conhecimento
)


def main():

    memoria = carregar_memoria()

    conhecimento = carregar_conhecimento()

    historico = []


    print("=" * 60)
    print("                 MINHA IA 0.3 🤖")
    print("=" * 60)

    print()

    print("Modelo: Qwen3 1.7B")

    print(
        "Memórias carregadas:",
        len(memoria)
    )

    print(
        "Informações carregadas:",
        len(conhecimento)
    )

    print()

    print("IA pronta! 🧠")

    print()


    while True:

        mensagem = input("Você: ").strip()


        if not mensagem:
            continue


        if mensagem.lower() == "sair":

            print()
            print("IA: Até mais! 👋")

            break


        if mensagem.lower().startswith("aprenda:"):

            conteudo = mensagem[
                len("aprenda:"):
            ].strip()


            if "=" not in conteudo:

                print()
                print(
                    "IA: Use assim:"
                )
                print(
                    "aprenda: nome = Maneiro"
                )
                print()

                continue


            chave, valor = conteudo.split(
                "=",
                1
            )


            resposta = aprender(
                chave,
                valor,
                memoria
            )


            print()
            print("IA:", resposta)
            print()

            continue


        if mensagem.lower().startswith("lembra:"):

            chave = mensagem[
                len("lembra:"):
            ].strip()


            resposta = lembrar(
                chave,
                memoria
            )


            print()
            print("IA:", resposta)
            print()

            continue


        try:

            print()
            print("IA: Pensando... 🤔")
            print()


            resposta = conversar(
                mensagem,
                memoria,
                historico,
                conhecimento
            )


            print("IA:", resposta)

            print()


            historico.append({
                "role": "user",
                "content": mensagem
            })


            historico.append({
                "role": "assistant",
                "content": resposta
            })


        except Exception as erro:

            print()
            print("❌ Erro:")
            print(erro)
            print()


if __name__ == "__main__":
    main()