import random
import string
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
            if viite.tagit.get('title') == title: ##Etsitään käyttäjän antamalla nimellä viitettä
                self._viitteet.remove(viite) ##Poistetaan viite listasta
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

    def tallenna(self, viite):
        for i, v in enumerate(self._viitteet):
            if v.tagit.get('title') == viite.tagit.get('title'):
                self._viitteet[i] = viite
                return viite

        self._viitteet.append(viite)
        return viite

    def anna_vapaa_viite_id(self, kirjoittaja, vuosi):
        def _anna_sattumanvarainen_id():
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        if kirjoittaja and vuosi:
            for viite in self._viitteet:
                if viite.anna_kirjoittaja() == kirjoittaja and viite.anna_vuosi() == vuosi:
                    return _anna_sattumanvarainen_id()
            return f"{kirjoittaja.replace(' ', '')}{vuosi}"

        return _anna_sattumanvarainen_id()
