from modulos import *
import math
from random import randint


def inicializar(nami):
    nami.get(
        "https://accounts.binance.com/pt-BR/login?return_to=aHR0cHM6Ly93d3cuYmluYW5jZS5jb20vcHQtQlI%3D"
    )
    sleep(15)
    nami.get("https://www.binance.com/pt-BR/trade/SHIB_BRL?layout=basic")
    sleep(7)
    brl_i, chz_i = saldos(nami)
    x1, x2 = x1x2(nami)
    chz_i_to_brl = chz_i * x1
    return brl_i, chz_i, x1, x2, chz_i_to_brl


def limpa_tela(beta, nami, vezes, effecinco, tempo, aba_aberta):
    beta += 1
    effecinco += 1
    if beta > vezes:
        clear_output()
        beta = 0

    if effecinco > 15:
        effecinco = 0
        aba_aberta = quando_falha(nami, aba_aberta)

    randomico = randint(tempo, tempo + 5)
    sleep(randomico)
    return beta, effecinco, aba_aberta


def saldos(nami):
    a = nami.find_elements_by_css_selector('span[class = "css-k4h8bj"]')
    sleep(0.3)
    brl_i = float(a[0].text[:-4])
    chz_i = float(a[1].text[:-4])
    return brl_i, chz_i


def od_venda(nami, x1, qtd, n, v, brl_i, chz_i):
    brl_f = brl_i + qtd * x1 * (1 - 0.001)
    chz_f = chz_i - qtd
    xi = x1

    v += 1
    n += 1
    return v, n, brl_f, chz_f, xi


def od_compra(nami, x2, qtd, n, c, brl_i, chz_i):
    brl_f = brl_i - qtd * x2
    chz_f = chz_i + qtd * (1 - 0.001)
    xi = x2

    c += 1
    n += 1
    return c, n, brl_f, chz_f, xi
