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
        laufzeit: Optional[int] = None,
        sondertilgung: Optional[int] = None,
        monatliche_rate: Optional[float] = None
    ):
        self.betrag = betrag
        self.tilgungssatz = tilgungssatz/100
        self.sollzins = sollzins/100
        self.laufzeit = laufzeit if laufzeit is not None else None
        self.sondertilgung = sondertilgung/12 if sondertilgung is not None else 0

        if monatliche_rate is not None:
            self.jahrliche_rate = monatliche_rate*12
            self.monatliche_rate = monatliche_rate
        else:
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
        m_laufzeit = self.laufzeit*12 if self.laufzeit is not None else None
        
        self.__zinsreihe.append(0)
        self.__tilgungsreihe.append(0)
        self.__restschuldreihe.append(restschuld)
        if m_laufzeit is not None:
            for _ in range(1, m_laufzeit + 1):
                zinsen = restschuld*m_sollzins
                tilgung = self.monatliche_rate - zinsen
                restschuld -= tilgung
                restschuld -= self.sondertilgung

                self.__zinsreihe.append(zinsen)
                self.__tilgungsreihe.append(tilgung)
                self.__restschuldreihe.append(restschuld)
        else:
            laufzeit_counter = 1
            while restschuld > 0:
                zinsen = restschuld*m_sollzins
                tilgung = self.monatliche_rate - zinsen
                restschuld -= tilgung
                restschuld -= self.sondertilgung

                self.__zinsreihe.append(zinsen)
                self.__tilgungsreihe.append(tilgung)
                self.__restschuldreihe.append(restschuld)
                laufzeit_counter += 1
            self.laufzeit = laufzeit_counter

    
    # @Decorators.check_month
    def tilgung_monat(self, monat: int) -> float:
        '''
        Tigungsbetrag an angegebene Monat
        '''
        return self.__tilgungsreihe[monat]


    # @Decorators.check_month
    def zinsen_monat(self, monat: int) -> float:
        '''
        Zinsbetrag an angegebene Monat
        '''
        return self.__zinsreihe[monat]


    # @Decorators.check_month
    def restschuld_monat(self, monat: int) -> float:
        '''
        Restschuld an angegebene Monat
        '''
        return self.__restschuldreihe[monat]

    # @Decorators.check_month
    def summe_zinsen(self, monat: Optional[int] = None) -> float:
        if monat is None:
            return sum(self.__zinsreihe)
        else:
            return sum(self.__zinsreihe[:monat])



