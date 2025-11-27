from entities.Viite import Viite


class ViiteRepository:
    def __init__(self):
        self._viitteet = []

    def luo(self, viite):
        self._viitteet.append(viite)

        return viite

    def anna(self):
        return self._viitteet
    
    def poista(self, title):
        for viite in self._viitteet:
            if viite.tagit.get('title') == title:
                self._viitteet.remove(viite)
                return True
        return False

    def osittaishaku(self, hakusana):
        hakusana = hakusana.lower()
        tulokset = []

        for viite in self._viitteet:
            title = viite.tagit.get('title', '').lower()
            if hakusana in title:
                tulokset.append(viite)
        
        return tulokset

