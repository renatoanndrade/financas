from modulos import *
import math


def taxa_transacao(metade_lucro, tx):
    return metade_lucro * tx


def taxar(lucro, tx):
    taxa = taxa_transacao(0.5 * lucro, tx)
    d_move = 0.5 * (lucro + taxa)
    return d_move


def vender(x1, chz_i, brl_i, l, tx):
    l = math.ceil(l)
    # Descobre o quanto tem que tranferir. Metade do lucro + metade da taxa
    d_move = taxar(l, tx)
    # extrai do chz_i a 0.5(lucro + taxa)
    chz_i += -d_move / x1
    # adcione o blr convertido à brl_i
    brl_i += d_move * (1 - tx)
    return brl_i, chz_i, math.ceil(d_move / x1)


def comprar(x2, chz_i, brl_i, l, tx):
    # Pega o valor ABSOLUTO do lucro para calcula a taxa. Lucro é negativo
    l = abs(l)
    # Coloca em numeros inteiros
    l = math.floor(l)
    # Descobre o quanto tem que tranferir. Metade do lucro + metade da taxa
    d_move = taxar(l, tx)
    # diminuir 0.5(lucro  + taxa) de brl_i. Isso pq o lucro já está em dinheiro
    brl_i += -d_move
    # adicione as acoes compradas à chz_i
    chz_i += (d_move / x2) * (1 - tx)
    return brl_i, chz_i, math.floor(d_move / x2)


def movimentando(x1, x2, xi, chz_i, brl_i, l, tx, status_movimentacao, n, v, c):
    if status_movimentacao == "pode_vender":
        v, n, brl_f, chz_f, xi = od_venda(nami, x1, qtd, n, v, brl_i, chz_i)
        return v, c, n, brl_f, chz_f, xi

    elif status_movimentacao == "pode_comprar":
        c, n, brl_f, chz_f, xi = od_compra(nami, x2, qtd, n, c, brl_i, chz_i)
        return v, c, n, brl_f, chz_f, xi
    else:
        return v, c, n, brl_i, chz_i, xi
