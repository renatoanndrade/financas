from modulos import *


def func(x):
    return "{:.3f}".format(x)


def x1x2(nami):
    try:
        a = nami.find_elements_by_css_selector('div[class = "bid-light"]')
        x1 = float(a[0].text)
        b = nami.find_elements_by_css_selector('div[class = "ask-light"]')
        x2 = float(b[-1].text)
        return x1, x2
    except:
        print("falou pegar X1 e X2")


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


def saldos(nami):
    a = nami.find_elements_by_css_selector('span[class = "css-k4h8bj"]')
    sleep(0.3)
    brl_i = float(a[0].text[:-4])
    chz_i = float(a[1].text[:-4])
    return brl_i, chz_i


def xii(nami, aba_aberta):

    try:
        if aba_aberta == False:
            a = nami.find_element_by_css_selector('div[id = "tab-2"]').click()
            sleep(2)
            nami.find_elements_by_css_selector(
                'div[class = "css-aregmd"]')[1].click()
            sleep(2)
            aba_aberta = True

        xi = float(
            nami.find_elements_by_css_selector(
                'div[class = "css-3je8bl"]')[1].text
        )

        return xi, aba_aberta
    except:
        aba_aberta = quando_falha(nami, aba_aberta)


def cabecalho(nami, chz_i, brl_i, xi, aba_aberta):
    # try:
    x1, x2 = x1x2(nami)
    state_delta_x = delta_x(xi, x1, x2)
    l, state_transation = lucro(chz_i, brl_i, x1, x2, state_delta_x)
    return xi, x1, x2, l, state_transation, aba_aberta


def delta_x(xi, x1, x2):
    delta_x1 = x1 - xi
    delta_x2 = x2 - xi
    return delta_x1, delta_x2



def lucro(chz_i, brl_i, x1, x2, state_delta_x):
    if state_delta_x == "pos":
        return chz_i - brl_i / x1, "vende"
    elif state_delta_x == "neg":
        return chz_i - brl_i / x2, "compra"
    else:
        return 0, "espera"


def vender(x1, chz_i, brl_i, l, tx):
    l = math.ceil(l)
    # Descobre o quanto tem que tranferir. Metade do lucro + metade da taxa
    d_move = taxar(l, tx)
    # extrai do chz_i a 0.5(lucro + taxa)
    chz_i += -d_move
    # adcione o blr convertido à brl_i
    brl_i += d_move * x1 * (1 - tx)
    return brl_i, chz_i, math.ceil(d_move)


def comprar(x2, chz_i, brl_i, l, tx):
    # Pega o valor ABSOLUTO do lucro para calcula a taxa. Lucro é negativo
    l = abs(l)
    # Coloca em numeros inteiros
    l = math.floor(l)
    # Descobre o quanto tem que tranferir. Metade do lucro + metade da taxa
    d_move = taxar(l, tx)
    # diminuir 0.5(lucro  + taxa) de brl_i. Isso pq o lucro já está em dinheiro
    brl_i += -d_move * x2
    # adicione as acoes compradas à chz_i
    chz_i += (d_move) * (1 - tx)
    return brl_i, chz_i, math.floor(d_move)


def imprimir_dados(delta_brl, delta_chz, brl_i, brl_f, chz_i, chz_f, modo, xi, luc):
    print(
        f"{modo} {[delta_brl, delta_chz, brl_i, brl_f, chz_i, chz_f, luc]}  {xi}")


def s_venda(x1, xi, chz_i, brl_i, l, valor_de_delta, ganho, luc, tx):
    if l / 2 > valor_de_delta:
        # simulando venda
        brl_t, chz_t, move_i = vender(x1, chz_i, brl_i, l, tx)
        # recalcular lucro simulado. tem que ser com xi, futuro
        chz_brl_f = chz_t * xi
        l2 = (chz_brl_f - brl_t) / xi

        # simulando a compra
        brl_f, chz_f, move_f = comprar(xi, chz_t, brl_t, l2, tx)
        delta_brl = brl_f - brl_i
        delta_chz = chz_f - chz_i
        modo = "v"
        imprimir_dados(delta_brl, delta_chz, brl_i,
                       brl_f, chz_i, chz_f, modo, xi, luc)
        if delta_brl > ganho and delta_chz > 0:
            return delta_brl, delta_chz, move_i
        else:
            return 0, 0, 0
    else:
        0, 0, 0


def s_compra(x2, xi, chz_i, brl_i, l, valor_de_delta, ganho, luc, tx):
    l = abs(l)
    if l / 2 > valor_de_delta:
        # simular compra
        brl_t, chz_t, move_i = comprar(x2, chz_i, brl_i, l, tx)
        # recalcular lucro simulado. tem que ser com xi, futuro
        chz_brl_f = chz_t * xi
        l2 = (chz_brl_f - brl_t) / xi
        # simular venda
        brl_f, chz_f, move_f = vender(xi, chz_t, brl_t, l2, tx)
        delta_brl = brl_f - brl_i
        delta_chz = chz_f - chz_i
        modo = "c"
        imprimir_dados(delta_brl, delta_chz, brl_i,
                       brl_f, chz_i, chz_f, modo, xi, luc)
        if delta_brl > ganho and delta_chz > 0:
            return delta_brl, delta_chz, move_i
        else:
            return 0, 0, 0
    else:
        return 0, 0, 0


def simulando(
    x1, x2, xi, chz_i, brl_i, l, state_transation, valor_de_delta, ganho, luc, tx
):
    if state_transation != "espera":
        if state_transation == "vende":
            delta_brl, delta_chz, qtd = s_venda(
                x1, xi, chz_i, brl_i, l, valor_de_delta, ganho, luc, tx
            )
            if delta_brl > 0 and delta_chz > 0:
                return "pode_vender", delta_brl, delta_chz, qtd
            else:
                return "espera", 0, 0, 0

        elif state_transation == "compra":
            delta_brl, delta_chz, qtd = s_compra(
                x2, xi, chz_i, brl_i, l, valor_de_delta, ganho, luc, tx
            )
            if delta_brl > 0 and delta_chz > 0:
                return "pode_comprar", delta_brl, delta_chz, qtd
            else:
                return "espera", 0, 0, 0
    else:
        return "espera", 0, 0, 0


def taxa_transacao(metade_lucro, tx):
    return metade_lucro * tx


def taxar(lucro, tx):
    taxa = taxa_transacao(0.5 * lucro, tx)
    d_move = 0.5 * (lucro + taxa)
    return d_move


def movimentando(
    nami, x1, x2, xi, chz_i, brl_i, qtd, status_movimentacao, n, v, c, luc, ganho, ini
):
    if status_movimentacao == "pode_vender":
        v, n, brl_f, chz_f, xi, luc, ganho, ini = od_venda(
            nami, x1, xi, qtd, n, v, brl_i, chz_i, luc, ganho, ini
        )
        return v, c, n, brl_f, chz_f, xi, luc, ganho, ini

    elif status_movimentacao == "pode_comprar":
        c, n, brl_f, chz_f, xi, luc, ganho, ini = od_compra(
            nami, x2, xi, qtd, n, c, brl_i, chz_i, luc, ganho, ini
        )
        return v, c, n, brl_f, chz_f, xi, luc, ganho, ini

    else:
        return v, c, n, brl_i, chz_i, xi, luc, ganho, ini


def od_venda(nami, x1, xi, qtd, n, v, brl_i, chz_i, luc, ganho, ini):
    brl_f = brl_i + qtd * x1 * (1 - 0.001)
    chz_f = chz_i - qtd
    luc += brl_f - brl_i + (chz_f - chz_i) * xi
    ganho += 1
    ini = time.time()
    xi = x1
    v += 1
    n += 1
    sleep(10)
    return v, n, brl_f, chz_f, xi, luc, ganho, ini


def od_compra(nami, x2, xi, qtd, n, c, brl_i, chz_i, luc, ganho, ini):
    brl_f = brl_i - qtd * x2
    chz_f = chz_i + qtd * (1 - 0.001)
    luc += brl_f - brl_i + (chz_f - chz_i) * xi
    ganho += 1
    ini = time.time()
    xi = x2
    c += 1
    n += 1
    sleep(10)
    return c, n, brl_f, chz_f, xi, luc, ganho, ini


def atualiza_ganho(ini, ganho, tempo):
    if ganho <= 0:
        ganho = 0
        return ganho, ini
    else:
        if time.time() - ini >= tempo:
            ganho += -0.2
            ini = time.time()
            if ganho < 0:
                ganho = 0
                return ganho, ini
            else:
                return ganho, ini
        else:
            return ganho, ini


def quando_falha(nami, aba_aberta):
    nami.refresh()
    aba_aberta = False
    sleep(5)
    return aba_aberta


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
