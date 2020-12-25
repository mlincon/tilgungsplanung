import numpy as np
import pandas as pd
import itertools

class Finanzierung:
    """
    betrag: kreditbetrag
    tilgungr: tilgungssatz bzw. tilgungsrate
    tilgungstart: tilgungsbeginn
    sollzins: jahrliche sollzins
    effzins: effektiver jahresollzins
    zb: zinsbindung (jahre)
    laufzeit: laufzeit (jahre)
    """
    def __init__(self, betrag, tilgungr, sollzins):
        self.darlehen = betrag
        self.tilgungr = tilgungr/100
        self.sollzins = sollzins/100
        self.__start_zinsen = 0
        self.__start_tilgung = 0

        self.jahrliche_rate = self.__jahrliche_rate()
        self.monatliche_rate = self.__monatliche_rate()

    def __jahrliche_rate(self):
        return self.darlehen*(self.tilgungr) + self.darlehen*(self.sollzins)

    def __monatliche_rate(self):
        return self.jahrliche_rate/12


    def tilgung_monat(self, monat):
        if monat == 0:
            return self.__start_tilgung
        else:
            zinsen = self.zinsen_monat(monat)
            return (self.monatliche_rate - zinsen)
    

    def zinsen_monat(self, monat):
        if monat == 0:
            return self.__start_zinsen
        else:
            saldo_vormonat = self.saldo_monat(monat - 1)
            tilgung_vormonat = self.tilgung_monat(monat - 1)
            return self.sollzins*(saldo_vormonat - tilgung_vormonat)/12

    
    def saldo_monat(self, monat):
        if monat == 0:
            return self.darlehen
        else:
            saldo_vormonat = self.saldo_monat(monat - 1)
            tilgung = self.tilgung_monat(monat)
            return saldo_vormonat - tilgung


if __name__=='__main__':

    fz = Finanzierung(
        betrag=479000,
        tilgungr=3,
        sollzins=0.92
    )

    print(round(fz.monatliche_rate, 2))
    print(round(fz.saldo_monat(1), 2))
    print(round(fz.zinsen_monat(2), 2))
