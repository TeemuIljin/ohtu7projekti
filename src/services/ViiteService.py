from pathlib import Path
import json

from entities.Viite import Viite


class ViiteService:
    OLETUS_DATA = Path("src/data/viitteet.json")
    OLETUS_BIB = Path("src/Lahteet.bib")

    def __init__(self, viite_repository):
        self._viite_repository = viite_repository
        self.viitetyypit = {
            "article": [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("lehti", "journal"),
                ("vuosi", "year"),
                ("vuosikerta", "volume"),
                ("sivut", "pages")
            ],
            "book": [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("vuosi", "year"),
                ("julkaisija", "publisher")
            ],
            "inproceedings": [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("vuosi", "year"),
                ("julkaisu", "booktitle")
            ]
        }

    def luo_viite(self, tyyppi, tagit):
        self._varmista_tyyppi(tyyppi)
        viite = self._rakenna_viite(tyyppi, tagit)
        return self._viite_repository.luo(viite)

    def anna_tagit(self, tyyppi):
        return self.viitetyypit[tyyppi]

    def anna_viitteet(self):
        return self._viite_repository.anna()

    def hae_viitteet_tiedostosta(self, polku=None):
        lahde = Path(polku) if polku else self.OLETUS_DATA
        sisalto = json.loads(lahde.read_text(encoding="utf-8"))

        if not isinstance(sisalto, list):
            raise ValueError("Datalähteen tulee olla lista viitteitä")

        lisatyt = 0
        for entry in sisalto:
            tyyppi = entry.get("type")
            tagit = entry.get("tags")
            if not tyyppi or not tagit:
                raise ValueError("Jokaisella viitteellä pitää olla type ja tags")

            self.luo_viite(tyyppi, tagit)
            lisatyt += 1

        return lisatyt

    def kirjoita_bibtex(self, polku=None):
        kohde = Path(polku) if polku else self.OLETUS_BIB
        kohde.parent.mkdir(parents=True, exist_ok=True)
        data = "\n\n".join(map(str, self.anna_viitteet()))
        kohde.write_text(data, encoding="utf-8")
        return kohde

    def _rakenna_viite(self, tyyppi, tagit):
        author = tagit.get("author")
        year = tagit.get("year")

        if not author or not year:
            raise ValueError("Kirjoittaja ja vuosi ovat pakolliset kentät")

        viite_id = f"{author.replace(' ', '')}{year}"
        return Viite(viite_id, tyyppi, tagit)

    def _varmista_tyyppi(self, tyyppi):
        if tyyppi not in self.viitetyypit:
            raise ValueError(f"Tuntematon viitetyyppi: {tyyppi}")
