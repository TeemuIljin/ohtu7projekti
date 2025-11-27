from entities.Viite import Viite


class ViiteRepository:
    def __init__(self):
        self._viitteet = []

    def luo(self, viite):
        self._viitteet.append(viite)

        return viite

    def anna(self):
        return self._viitteet
    
    def etsi(self, muokattava):
        for viite in self._viitteet:
            if viite.tagit.get('title') == muokattava:
                return viite
        return "Viitettä ei löytynyt."
    
    def poista(self, title):
        for viite in self._viitteet:
            if viite.tagit.get('title') == title:
                self._viitteet.remove(viite)
                return True
        return False

    def tallenna(self, viite):
        for i, v in enumerate(self._viitteet):
            if v.tagit.get('title') == viite.tagit.get('title'):
                self._viitteet[i] = viite
                return viite

        self._viitteet.append(viite)
        return viite
