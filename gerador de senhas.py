"""Gerador de senhas seguras"""

import argparse
import secrets
import string

MINUSCULA = string.ascii_lowercase
MAIUSCULA = string.ascii_uppercase
NUMERO = string.digits
SIMBOLOS = "!@#$%&*()-_=+[]{};:,.<>?/"
AMBIGUOS = "0O1lI|"


def gerar_senha(
        tamanho=16,
        minusculas=True,
        maiusculas=True,
        numeros=True,
        simbolos=True,
        sem_ambiguos=False,
):
    """Gera uma senha aleatória e segura.
    Garante pelo menos um caractere de cada categoria selecionada."""
    categorias = []
    if minusculas:
        categorias.append(MINUSCULA)
    if maiusculas:
        categorias.append(MAIUSCULA)
    if numeros:
        categorias.append(NUMERO)
    if simbolos:
        categorias.append(SIMBOLOS)

    if sem_ambiguos:
        categorias = ["".join(c for c in cat if c not in AMBIGUOS) for cat in categorias]

    if not categorias:
        raise ValueError("Selecione pelo menos um tipo de caractere.")
    if tamanho < len(categorias):
        raise ValueError(
            f"O tamanho mínimo para essa combinação é {len(categorias)}."
        )

    todos = "".join(categorias)

    # Um caractere de cada categoria + restante aleatório do conjunto total
    senha = [secrets.choice(cat) for cat in categorias]
    senha += [secrets.choice(todos) for _ in range(tamanho - len(senha))]

    # Embaralhar com gerador seguro (Fisher-Yates)
    for i in range(len(senha) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        senha[i], senha[j] = senha[j], senha[i]

    return "".join(senha)


def avaliar_forca(senha):
    """Retorna uma classificação simples de força de senha."""
    pontos = 0
    pontos += len(senha) >= 12
    pontos += len(senha) >= 16
    pontos += any(c in MINUSCULA for c in senha)
    pontos += any(c in MAIUSCULA for c in senha)
    pontos += any(c in NUMERO for c in senha)
    pontos += any(c in SIMBOLOS for c in senha)

    if pontos <= 3:
        return "Fraca"
    if pontos <= 5:
        return "Média"
    return "Forte"


def sim_nao(pergunta, padrao=True):
    sufixo = " [S/n]: " if padrao else " [s/N]: "
    resposta = input(pergunta + sufixo).strip().lower()
    if not resposta:
        return padrao
    return resposta in ("s", "sim", "y", "yes")


def modo_interativo():
    print("=== Gerador de Senhas ===\n")
    try:
        tamanho = int(input("Tamanho da senha [16]: ") or 16)
    except ValueError:
        print("Valor inválido, usando 16.")
        tamanho = 16

    minusculas = sim_nao("Incluir letras minúsculas?")
    maiusculas = sim_nao("Incluir letras maiúsculas?")
    numeros = sim_nao("Incluir números?")
    simbolos = sim_nao("Incluir símbolos?")
    sem_ambiguos = sim_nao("Evitar caracteres ambíguos (0, O, 1, l, I)?", padrao=False)

    try:
        quantidade = int(input("Quantidade de senhas [1]: ") or 1)
    except ValueError:
        quantidade = 1

    print()
    try:
        for _ in range(quantidade):
            senha = gerar_senha(tamanho, minusculas, maiusculas, numeros, simbolos, sem_ambiguos)
            print(f"{senha}   ({avaliar_forca(senha)})")
    except ValueError as erro:
        print(f"Erro: {erro}")


def main():
    parser = argparse.ArgumentParser(description="Gerador de senhas seguras.")
    parser.add_argument("-t", "--tamanho", type=int, default=16, help="tamanho da senha (padrão: 16)")
    parser.add_argument("-q", "--quantidade", type=int, default=1, help="quantidade de senhas (padrão: 1)")
    parser.add_argument("--sem-minusculas", action="store_true", help="não usar letras minúsculas")
    parser.add_argument("--sem-maiusculas", action="store_true", help="não usar letras maiúsculas")
    parser.add_argument("--sem-numeros", action="store_true", help="não usar números")
    parser.add_argument("--sem-simbolos", action="store_true", help="não usar símbolos")
    parser.add_argument("--sem-ambiguos", action="store_true", help="evitar caracteres parecidos (0, O, 1, l, I)")
    parser.add_argument("-i", "--interativo", action="store_true", help="modo interativo")
    args = parser.parse_args()

    if args.interativo:
        modo_interativo()
        return

    try:
        for _ in range(args.quantidade):
            senha = gerar_senha(
                tamanho=args.tamanho,
                minusculas=not args.sem_minusculas,
                maiusculas=not args.sem_maiusculas,
                numeros=not args.sem_numeros,
                simbolos=not args.sem_simbolos,
                sem_ambiguos=args.sem_ambiguos,
            )
            print(f"{senha}   ({avaliar_forca(senha)})")
    except ValueError as erro:
        parser.error(str(erro))


if __name__ == "__main__":
    main()