import numpy as np
import pandas as pd

from decorators import Decorators
class Finanzierung:
    """
    betrag: kreditbetrag
    tilgungssatz: tilgungssatz bzw. tilgungsrate
    tilgungsbeginn: tilgungsbeginn (mm.yyyy)
    sollzins: jahrliche sollzins
    effzins: effektiver jahresollzins
    zb: zinsbindung (jahre)
    laufzeit: laufzeit (jahre)
    """
    def __init__(
        self, 
        betrag, 
        tilgungssatz, 
        sollzins, 
        laufzeit
    ):
        self.betrag = betrag
        self.tilgungssatz = tilgungssatz/100
        self.sollzins = sollzins/100
        self.laufzeit = laufzeit

        self.jahrliche_rate = self.__jahrliche_rate()
        self.monatliche_rate = self.__monatliche_rate()

        self.__zinsreihe = []
        self.__tilgungsreihe = []
        self.__saldoreihe = []
        self.__reihen()


    def __jahrliche_rate(self):
        '''
        Jahrliche Zahlungsbetrag
        '''
        return self.betrag*(self.sollzins + self.tilgungssatz)

    def __monatliche_rate(self):
        '''
        Monatlich Zahlungsbetrag
        '''
        return self.jahrliche_rate/12


    def __reihen(self):
        '''
        Monatliche Betrag von Zins, Tilgung und Restschuld
        '''
        saldo = self.betrag
        m_sollzins = self.sollzins/12
        m_laufzeit = self.laufzeit*12
        
        self.__zinsreihe.append(0)
        self.__tilgungsreihe.append(0)
        self.__saldoreihe.append(saldo)
        for _ in range(1, m_laufzeit + 1):
            zinsen = saldo*m_sollzins
            tilgung = self.monatliche_rate - zinsen
            saldo -= tilgung

            self.__zinsreihe.append(zinsen)
            self.__tilgungsreihe.append(tilgung)
            self.__saldoreihe.append(saldo)

    
    @Decorators.check_month
    def tilgung_monat(self, monat):
        '''
        Tigungsbetrag an angegebene Monat
        '''
        return self.__tilgungsreihe[monat]


    @Decorators.check_month
    def zinsen_monat(self, monat):
        '''
        Zinsbetrag an angegebene Monat
        '''
        return self.__zinsreihe[monat]


    @Decorators.check_month
    def saldo_monat(self, monat):
        '''
        Restschuld an angegebene Monat
        '''
        return self.__saldoreihe[monat]





if __name__=='__main__':

    fz = Finanzierung(
        betrag=479000,
        tilgungssatz=3,
        sollzins=0.92,
        laufzeit=29
    )

    print(round(fz.monatliche_rate, 2))
    print(round(fz.saldo_monat(120), 2))
    print(round(fz.zinsen_monat(1), 2))
    print(round(fz.zinsen_monat(120.2312), 2))
