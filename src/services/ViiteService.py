from entities.Viite import Viite


class ViiteService:
    def __init__(self, viite_repository):
        self._viite_repository = viite_repository
        self.viitetyypit = {
            "article": ["author", "title", "journal", "year", "volume", "pages"],
            "book": ["author", "title", "year", "publisher"],
            "inproceedings": ["author", "title", "year", "booktitle"]
        }

    def luo_viite(self, tyyppi, tagit):
        return self._viite_repository.luo(
            Viite(tagit['author'].replace(" ", "") +
                  tagit['year'], tyyppi, tagit)
        )

    def anna_tagit(self, tyyppi):
        return self.viitetyypit[tyyppi]

    def anna_viitteet(self):
        return self._viite_repository.anna()
    
    def poista_viite(self, tunniste):
        return self._viite_repository.poista(tunniste)
