from entities.Viite import Viite


class ViiteRepository:
    def __init__(self):
        self._viitteet = []

    def luo(self, viite):
        self._viitteet.append(viite)

        return viite

    def anna(self):
        return self._viitteet


# -> klo 12.13
# klo 14.57 ->
