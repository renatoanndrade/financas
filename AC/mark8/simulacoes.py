import pandas as pd
from time import sleep
from random import randint
import math
from selenium.webdriver import Firefox
from IPython.display import clear_output

from cond_init import *
from nami_navega import *
from transacao import *
from funcs import *


def func(x):
    return "{:.3f}".format(x)


def s_venda(x1, xi, chz_i, brl_i, l, tx):
    # simulando venda
    brl_t, chz_t, x = vender(x1, chz_i, brl_i, l, tx)
    # recalcular lucro simulado. tem que ser com xi, futuro
    chz_brl_f = chz_t * xi
    l2 = chz_brl_f - brl_t
    # simulando a compra
    brl_f, chz_f, x = comprar(xi, chz_t, brl_t, l2, tx)
    delta_brl = brl_f - brl_i
    delta_chz = chz_f - chz_i
    return delta_brl, delta_chz


def s_compra(x2, xi, chz_i, brl_i, l, tx):
    # simular compra
    brl_t, chz_t, x = comprar(x2, chz_i, brl_i, l, tx)
    # recalcular lucro simulado. tem que ser com xi, futuro
    chz_brl_f = chz_t * xi
    l2 = chz_brl_f - brl_t
    # simular venda
    brl_f, chz_f, x = vender(xi, chz_t, brl_t, l2, tx)
    delta_brl = brl_f - brl_i
    delta_chz = chz_f - chz_i
    return delta_brl, delta_chz


def simulando(x1, x2, xi, chz_i, brl_i, l, state_transation, tx):
    if state_transation != "espera":
        if state_transation == "vende":
            delta_brl, delta_chz = s_venda(x1, xi, chz_i, brl_i, l, tx)
            if delta_brl > 0 and delta_chz > 0:
                return "pode_vender"
            else:
                return "espera"
        elif state_transation == "compra":
            delta_brl, delta_chz = s_compra(x2, xi, chz_i, brl_i, l, tx)
            if delta_brl > 0 and delta_chz > 0:
                return "pode_comprar"
            else:
                return "espera"
    else:
        return "espera"
