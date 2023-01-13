from modulos import *


def arredondar(x):
    return "{:.3f}".format(x)


TX = 0.001
INTERVALO = 60


class Logar:
    def __init__(self, nami):
        self.nami = nami
        self.loggar()

    def loggar(self):
        self.nami.get(
            "https://accounts.binance.com/pt-BR/login?return_to=aHR0cHM6Ly93d3cuYmluYW5jZS5jb20vcHQtQlI%3D"
        )


class Func:
    def __init__(self, nami, lucro):
        self.nami = nami
        self.chz_i = 0
        self.brl_i = 0
        self.xi = 0
        self.xii()
        self.aba_aberta = False
        self.saldos()
        self.x1x2()
        self.delta_x()
        self.somatorio_brl = 0
        self.somatorio_chz = 0
        self.lucro = lucro
        self.taxa_ganho = 1
        self.t_i = time.time()
        self.fator = 0

    def decresce_ganho(self):
        if self.taxa_ganho <= 0.35:
            self.taxa_ganho = 0
        else:
            if time.time() - self.t_i >= INTERVALO:
                self.taxa_ganho += -0.2
                self.t_i = time.time()
        self.fator += -1
        if self.fator <= 0:
            self.fator = 0

    def aumenta_ganho(self):
        self.taxa_ganho += (1 + self.fator)**self.fator
        self.t_i = time.time()
        self.fator += 1

    def quando_falha(self):
        self.nami.refresh()
        self.aba_aberta = False
        print('quando falha')
        sleep(5)

    def xii(self):
        self.nami.find_element_by_css_selector('div[id = "tab-2"]').click()
        sleep(2)
        self.nami.find_elements_by_css_selector(
            'div[class = "css-aregmd"]')[1].click()
        sleep(2)
        self.xi = float(self.nami.find_elements_by_css_selector(
            'div[class = "css-3je8bl"]')[1].text)

    def x1x2(self):
        try:
            a = self.nami.find_elements_by_css_selector(
                'div[class = "bid-light"]')
            self.x1 = abs(float(a[0].text))
            b = self.nami.find_elements_by_css_selector(
                'div[class = "ask-light"]')
            self.x2 = abs(float(b[-1].text))
        except:
            print("falou pegar X1 e X2")

    def saldos(self):
        a = self.nami.find_elements_by_css_selector(
            'span[class = "css-k4h8bj"]')
        sleep(0.3)
        self.brl_i = float(a[0].text[:-4])
        self.chz_i = float(a[1].text[:-4])

    def delta_x(self):
        self.delta_x1 = abs(self.x1 - self.xi)
        self.delta_x2 = abs(self.x2 - self.xi)

    def trans(self, brl, chz, xf):
        return abs(0.5*(chz*xf - brl)*(1+TX))

    def vender(self, brl, chz, transf, xf):
        brl += transf*(1-TX)
        chz += -transf/xf
        return brl, chz

    def comprar(self, brl, chz, transf, xf):
        brl += -transf
        chz += (transf/xf)*(1-TX)
        return brl, chz

    def s_venda(self):
        transf = self.trans(self.brl_i, self.chz_i, self.x1)
        brl_t, chz_t = self.vender(self.brl_i, self.chz_i, transf, self.x1)

        transf = self.trans(brl_t, chz_t, self.xi)
        brl_f, chz_f = self.comprar(brl_t, chz_t, transf, self.xi)

        delta_brl = brl_f - self.brl_i
        delta_chz = chz_f - self.chz_i
        return delta_brl, delta_chz

    def s_compra(self):
        transf = self.trans(self.brl_i, self.chz_i, self.x2)
        brl_t, chz_t = self.comprar(self.brl_i, self.chz_i, transf, self.x2)

        transf = self.trans(brl_t, chz_t, self.xi)
        brl_f, chz_f = self.vender(brl_t, chz_t, transf, self.xi)

        delta_brl = brl_f - self.brl_i
        delta_chz = chz_f - self.chz_i
        return delta_brl, delta_chz

    def simular(self):
        self.x1x2()
        delta_brl_v, delta_chz_v = self.s_venda()
        delta_brl_c, delta_chz_c = self.s_compra()

        x = [delta_brl_v, delta_chz_v]
        y = list(map(arredondar, x))
        print('v', y)
        x = [delta_brl_c, delta_chz_c]
        y = list(map(arredondar, x))
        print('c', y)

        if (delta_brl_v > self.taxa_ganho and delta_chz_v > 0):
            return 'venda_liberada', delta_brl_v, delta_chz_v
        elif (delta_brl_c > self.taxa_ganho and delta_chz_c > 0):
            return 'compra_liberada', delta_brl_c, delta_chz_c
        else:
            return 'espera', 0, 0

    def od_venda(self, x1, qtd):
        self.nami.find_element_by_css_selector(
            'input[id = "FormRow-SELL-price"]').clear()
        self.nami.find_element_by_css_selector(
            'input[id = "FormRow-SELL-quantity"]').clear()
        self.nami.find_element_by_css_selector(
            'input[id = "FormRow-SELL-price"]').send_keys(str(x1))
        self.nami.find_element_by_css_selector(
            'input[id = "FormRow-SELL-quantity"]').send_keys(str(qtd))
        sleep(3)
        self.nami.find_element_by_css_selector(
            'button[id = "orderformSellBtn"]').click()
        sleep(3)
        self.nami.refresh()
        sleep(7)
        self.saldos()

    def od_compra(self, x2, qtd):
        self.nami.find_element_by_css_selector(
            'input[id = "FormRow-BUY-price"]').clear()
        self.nami.find_elements_by_css_selector(
            'input[id = "FormRow-BUY-quantity"]')[0].clear()
        self.nami.find_element_by_css_selector(
            'input[id = "FormRow-BUY-price"]').send_keys(str(x2))
        self.nami.find_elements_by_css_selector(
            'input[id = "FormRow-BUY-quantity"]')[0].send_keys(str(qtd))

        sleep(1)
        self.nami.find_element_by_css_selector(
            'button[id = "orderformBuyBtn"]').click()
        sleep(3)
        self.nami.refresh()
        sleep(7)
        self.saldos()

    def operacao(self):
        opera, delta_brl, delta_chz = self.simular()

        if opera == 'venda_liberada':
            transf = self.trans(self.brl_i, self.chz_i, self.x1)
            print(transf)
            #self.brl_i, self.chz_i = self.vender(self.brl_i, self.chz_i, transf, self.x1)
            if transf > 10:
                qtd = math.ceil(transf/self.x1)
                print(qtd)
                self.od_venda(self.x1, qtd)
                self.somatorio_brl += delta_brl
                self.somatorio_chz += delta_chz
                self.xii()
                self.aumenta_ganho()
                opera == 'espera'

        elif opera == 'compra_liberada':
            transf = self.trans(self.brl_i, self.chz_i, self.x2)
            print(transf)
            if transf > 10:
                #self.brl_i, self.chz_i = self.comprar(self.brl_i, self.chz_i, transf, self.x2)
                qtd = math.floor(transf/self.x2)
                print(qtd)
                self.od_compra(self.x2, qtd)
                self.xii()
                self.somatorio_brl += delta_brl
                self.somatorio_chz += delta_chz
                self.aumenta_ganho()
                opera == 'espera'

    def rodar(self):
        while True:
            self.x1x2
            self.operacao()
            self.decresce_ganho()
            x = [self.brl_i, self.chz_i, self.somatorio_brl,
                 self.somatorio_chz, self.taxa_ganho]
            y = list(map(arredondar, x))
            print(y,  self.xi, self.x1)
            sleep(30)
            clear_output()
