from pathlib import Path
import json

from src.entities.Viite import Viite


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
                ("vuosi", "year")
            ],

            ("kirja", "book"): [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("julkaisija", "publisher"),
                ("vuosi", "year")
            ],

            ("vihkonen", "booklet"): [
                ("teoksen nimi", "title")
            ],

            ("kirjan osa", "inbook"): [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("julkaisija", "publisher"),
                ("vuosi", "year")
            ],

            ("artikkeli kirjassa", "incollection"): [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("julkaisu", "booktitle"),
                ("julkaisija", "publisher"),
                ("vuosi", "year")
            ],

            ("konferenssi", "inproceedings"): [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("julkaisu", "booktitle"),
                ("vuosi", "year")
            ],

            ("konferenssi", "conference"): [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("julkaisu", "booktitle"),
                ("vuosi", "year")
            ],

            ("käsikirja", "manual"): [
                ("teoksen nimi", "title"),
                ("vuosi", "year")
            ],

            ("pro gradu", "mastersthesis"): [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("oppilaitos", "school"),
                ("vuosi", "year")
            ],

            ("väitöskirja", "phdthesis"): [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("oppilaitos", "school"),
                ("vuosi", "year")
            ],

            ("tekninen raportti", "techreport"): [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("organisaatio", "institution"),
                ("vuosi", "year")
            ],

            ("sekalaista", "misc"): [],

            ("julkaisukokoelma", "proceedings"): [
                ("teoksen nimi", "title"),
                ("vuosi", "year")
            ],

            ("julkaisematon", "unpublished"): [
                ("kirjoittaja", "author"),
                ("teoksen nimi", "title"),
                ("huomautus", "note")
            ]
        }

        self.tagityypit = {
            "osoite": "address",
            "lisähuomautus": "annote",
            "kirjoittaja": "author",
            "julkaisu": "booktitle",
            "luku": "chapter",
            "painos": "edition",
            "toimittaja": "editor",
            "julkaisumuoto": "howpublished",
            "laitos": "institution",
            "lehti": "journal",
            "kuukausi": "month",
            "huomautus": "note",
            "numero": "number",
            "organisaatio": "organization",
            "sivut": "pages",
            "julkaisija": "publisher",
            "oppilaitos": "school",
            "sarja": "series",
            "teoksen nimi": "title",
            "tyyppi": "type",
            "vuosikerta": "volume",
            "vuosi": "year",
            "kategoria": "category"
        }

    def anna_fi_nimi_ja_bib_nimi(self, tagi):
        """
        Palauttaa monikon, jossa on tagin
        suomenkielinen nimi ja bibtex-nimi

        :param tagi: tagi, jonka mukaan haetaan
        """
        for tagi_nimet in self.tagityypit.items():
            if tagi in tagi_nimet:
                return tagi_nimet

        return (None, None)

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
        return (None, None)

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
        poistettu = self._viite_repository.poista(tunniste)
        if poistettu:
            self.kirjoita_bibtex()
        return poistettu

    def muokkaa_tagia(self, muokattava, tagi, arvo):
        viitteet = self._viite_repository.anna()
        for v in viitteet:
            if v.tagit.get("title") == muokattava:
                v.tagit[tagi] = arvo
                # päivitä repositoryssa (tallenna korvaamalla)
                try:
                    self._viite_repository.tallenna(v)
                except Exception:
                    # jos repository ei tue tallenna, varmuuden vuoksi jätetään muutos paikalliseen olioon
                    pass
                # päivitä Lahteet.bib jos tarpeen
                try:
                    self.kirjoita_bibtex()
                except Exception:
                    pass
                return True
        return False

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
        kirjoittaja = tagit.get("author")
        vuosi = tagit.get("year")

        viite_id = self._viite_repository.anna_vapaa_viite_id(kirjoittaja, vuosi)

        return Viite(viite_id, tyyppi, tagit)

    def _varmista_tyyppi(self, tyyppi):
        if not self.anna_tagit_ja_bib_tyyppi(tyyppi):
            raise ValueError(f"Tuntematon viitetyyppi: {tyyppi}")

    def hae_nimea(self, hakusana):
        tulokset = self._viite_repository.osittaishaku(hakusana)

        return sorted(
            tulokset,
            key=lambda v: (
                v.tyyppi.lower(),
                v.tagit.get("title", "").lower()
            )
        )
        
    def suodata(self, tyyppi=None, vuosi=None, kirjoittaja=None):
        """
        Suodattaa viitteet annettujen kriteerien perusteella.

        :param tyyppi: Viitteen tyyppi (esim. "book", "article")
        :param vuosi: Julkaisuvuosi
        :param kirjoittaja: Kirjoittajan nimi (osittaishaku)
        :return: Lista suodatetuista viitteistä
        """
        viitteet = self._viite_repository.anna()
        tulokset = []

        for viite in viitteet:
            # Tarkista tyyppi
            if tyyppi and viite.tyyppi.lower() != tyyppi.lower():
                continue

            # Tarkista vuosi
            if vuosi and viite.tagit.get("year") != vuosi:
                continue

            # Tarkista kirjoittaja (osittaishaku)
            if kirjoittaja:
                viite_kirjoittaja = viite.tagit.get("author", "").lower()
                if kirjoittaja.lower() not in viite_kirjoittaja:
                    continue

            tulokset.append(viite)

        return sorted(
            tulokset,
            key=lambda v: (
                v.tyyppi.lower(),
                v.tagit.get("title", "").lower()
            )
        )
        
    def hae_kategoriaa(self, kategoria):
        viitteet = self._viite_repository.kategoriahaku(kategoria)
        return sorted(
            viitteet,
            key=lambda v: (
                v.tyyppi.lower(),
                v.tagit.get("category", "").lower()
            )
        )
    
