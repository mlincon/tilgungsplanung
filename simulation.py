import locale
locale.setlocale(locale.LC_ALL, 'de_DE')

from typing import Optional
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
        betrag: int, 
        tilgungssatz: float, 
        sollzins: float, 
        laufzeit: int
    ):
        self.betrag = betrag
        self.tilgungssatz = tilgungssatz/100
        self.sollzins = sollzins/100
        self.laufzeit = laufzeit

        self.jahrliche_rate = self.__berechne_jahrliche_rate()
        self.monatliche_rate = self.__berechne_monatliche_rate()

        self.__zinsreihe = []
        self.__tilgungsreihe = []
        self.__restschuldreihe = []
        self.__berechne_reihen()


    def __berechne_jahrliche_rate(self) -> float:
        '''
        Jahrliche Zahlungsbetrag
        '''
        return self.betrag*(self.sollzins + self.tilgungssatz)

    def __berechne_monatliche_rate(self) -> float:
        '''
        Monatlich Zahlungsbetrag
        '''
        return self.jahrliche_rate/12


    def __berechne_reihen(self) -> None:
        '''
        Monatliche Betrag von Zins, Tilgung und Restschuld
        '''
        restschuld = self.betrag
        m_sollzins = self.sollzins/12
        m_laufzeit = self.laufzeit*12
        
        self.__zinsreihe.append(0)
        self.__tilgungsreihe.append(0)
        self.__restschuldreihe.append(restschuld)
        for _ in range(1, m_laufzeit + 1):
            zinsen = restschuld*m_sollzins
            tilgung = self.monatliche_rate - zinsen
            restschuld -= tilgung

            self.__zinsreihe.append(zinsen)
            self.__tilgungsreihe.append(tilgung)
            self.__restschuldreihe.append(restschuld)

    
    @Decorators.check_month
    def tilgung_monat(self, monat: int) -> float:
        '''
        Tigungsbetrag an angegebene Monat
        '''
        return self.__tilgungsreihe[monat]


    @Decorators.check_month
    def zinsen_monat(self, monat: int) -> float:
        '''
        Zinsbetrag an angegebene Monat
        '''
        return self.__zinsreihe[monat]


    @Decorators.check_month
    def restschuld_monat(self, monat: int) -> float:
        '''
        Restschuld an angegebene Monat
        '''
        return self.__restschuldreihe[monat]

    @Decorators.check_month
    def summe_zinsen(self, monat: Optional[int] = None) -> float:
        if monat is None:
            return sum(self.__zinsreihe)
        else:
            return sum(self.__zinsreihe[:monat])



if __name__=='__main__':

    fz_10 = Finanzierung(
        betrag=479000,
        tilgungssatz=3,
        sollzins=0.92,
        laufzeit=29
    )
    fz_15 = Finanzierung(
        betrag=479000,
        tilgungssatz=3,
        sollzins=1.22,
        laufzeit=29
    )
    fz_20 = Finanzierung(
        betrag=479000,
        tilgungssatz=3,
        sollzins=1.56,
        laufzeit=29
    )

    print(round(fz_10.monatliche_rate, 2))
    print(round(fz_15.monatliche_rate, 2))
    print(round(fz_20.monatliche_rate, 2))

    print(fz_10.summe_zinsen(15*12))
    print(fz_10.restschuld_monat(15*12))

    print(fz_15.summe_zinsen(15*12))
    print(fz_15.restschuld_monat(15*12))

    print(fz_20.summe_zinsen(15*12))
    print(fz_20.restschuld_monat(15*12))

