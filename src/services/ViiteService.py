from pathlib import Path
import json

from entities.Viite import Viite


class ViiteService:
    OLETUS_DATA = Path("src/data/viitteet.json")
    OLETUS_BIB = Path("src/Lahteet.bib")

    def __init__(self, viite_repository):
        self._viite_repository = viite_repository
        self.viitetyypit = {
            ("artikkeli", "article"): [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("lehti", "journal"),
                ("vuosi", "year"),
                ("vuosikerta", "volume"),
                ("sivut", "pages")
            ],
            ("kirja", "book"): [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("vuosi", "year"),
                ("julkaisija", "publisher")
            ],
            ("konferenssi", "inproceedings"): [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("vuosi", "year"),
                ("julkaisu", "booktitle")
            ]
        }

    def luo_viite(self, tyyppi, tagit):
        self._varmista_tyyppi(tyyppi)
        viite = self._rakenna_viite(tyyppi, tagit)
        luotu_viite = self._viite_repository.luo(viite)
        self.kirjoita_bibtex()
        return luotu_viite

    def anna_tagit_ja_bib_tyyppi(self, tyyppi):
        for tyyppi_nimet, tagit in self.viitetyypit.items():
            if tyyppi in tyyppi_nimet:
                return (tyyppi_nimet[1], tagit)
        return None

    def anna_viitteet(self):
        viitteet = self._viite_repository.anna()

        return sorted(
            viitteet,
            key=lambda v: (
                v.tyyppi.lower(),
                v.tagit.get("title", "").lower()
            )
        )
        
    def poista_viite(self, tunniste):
        return self._viite_repository.poista(tunniste)

    def muokkaa_tagia(self, muokattava, tagi, arvo):
        viite = self._viite_repository.etsi(muokattava)

        if tagi not in viite.tagit:
            for _, tagiparit in self.viitetyypit.items():
                for fi_nimi, bib_nimi in tagiparit:
                    if fi_nimi == tagi:
                        tagi = bib_nimi
                        break
                if tagi in viite.tagit:
                    break
                
        if viite and tagi in viite.tagit:
            viite.tagit[tagi] = arvo
            self._viite_repository.tallenna(viite)
            self.kirjoita_bibtex()
            return viite

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
                raise ValueError(
                    "Jokaisella viitteellä pitää olla type ja tags")

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
        if not self.anna_tagit_ja_bib_tyyppi(tyyppi):
            raise ValueError(f"Tuntematon viitetyyppi: {tyyppi}")
