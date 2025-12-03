import json
from pathlib import Path
import tempfile

from repositories.ViiteRepository import ViiteRepository
from services.ViiteService import ViiteService


def luo_palvelu():
    return ViiteService(ViiteRepository())


def test_hae_viitteet_tiedostosta():
    entries = [
        {
            "type": "book",
            "tags": {
                "author": "Minna Canth",
                "title": "Työmiehen vaimo",
                "year": "1885",
                "publisher": "WSOY"
            }
        }
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        polku = Path(tmpdir) / "lahde.json"
        polku.write_text(json.dumps(entries), encoding="utf-8")

        service = luo_palvelu()
        maara = service.hae_viitteet_tiedostosta(polku)

        assert maara == 1
        assert len(service.anna_viitteet()) == 1


def test_kirjoita_bibtex_luo_tiedoston():
    service = luo_palvelu()
    service.luo_viite(
        "book",
        {
            "author": "Antti Tuuri",
            "title": "Talvisota",
            "year": "1984",
            "publisher": "Otava"
        }
    )

    with tempfile.TemporaryDirectory() as tmpdir:
        kohde = Path(tmpdir) / "lahteet.bib"
        service.kirjoita_bibtex(kohde)

        sisalto = kohde.read_text(encoding="utf-8")
        assert "AnttiTuuri1984" in sisalto


def test_luo_viite():
    service = luo_palvelu()
    tyyppi = "book"
    tagit = {
        "author": "Testi Testinen",
        "title": "Missä on puu?",
        "year": "1997",
        "publisher": "WSOY"
    }

    viite = service.luo_viite(tyyppi, tagit)
    viite_str = str(viite)

    assert viite_str.startswith("@book{TestiTestinen1997,")
    assert "author = {Testi Testinen}," in viite_str
    assert "title = {Missä on puu?}," in viite_str
    assert "year = {1997}," in viite_str
    assert "publisher = {WSOY}" in viite_str
    assert viite_str.endswith("}")


def test_anna_tagit_ja_bib_tyyppi():
    service = luo_palvelu()

    (bib_tyyppi, tagit) = service.anna_tagit_ja_bib_tyyppi("kirja")

    assert bib_tyyppi == "book"
    assert tagit == [
        ("kirjoittaja", "author"),
        ("teoksen nimi", "title"),
        ("julkaisija", "publisher"),
        ("vuosi", "year")
    ]

def test_poista_viite():
    service = luo_palvelu()

##Luodaan uusi viite
    service.luo_viite(
        "book",
        {
            "author": "Antti Tuuri",
            "title": "Talvisota",
            "year": "1984",
            "publisher": "Otava"
        })

##Poistetaan viite    
    service.poista_viite("Talvisota")

##Tarkistetaan etä viite on poistunut
    viitteet = service.anna_viitteet()

    assert len(viitteet) == 0

def test_poista_kun_viitettä_ei_ole():
    service = luo_palvelu()

    result = service.poista_viite("tommone")

    assert result is False
