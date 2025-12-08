import json
from pathlib import Path
import tempfile

from src.repositories.ViiteRepository import ViiteRepository
from src.services.ViiteService import ViiteService


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
    
def test_hae_nimella_kun_nimia_loytyy():
    service= luo_palvelu()
    #luodaan viitteita hakua varten
    v1 = service.luo_viite(
        "book",
        {
            "author": "kirjoittaja",
            "title": "Testiteos",
            "year": "2000",
            "publisher": "Otava"
        })
    v2 = service.luo_viite(
        "book",
        {
            "author": "kirjailija",
            "title": "teostesti2",
            "year": "2001",
            "publisher": "Otava"
        })

    #suoritetaan haku
    tulos = service.hae_nimea("testi")
    #heattujen viitteiden tulisi olla samat kuin alussa luodut viitteet ja aakkosjärjestyksessä
    assert tulos == sorted([v1, v2], key=lambda v: v.tagit["title"].lower())

def test_hae_nimella_kun_ei_ole_nimia():
    service= luo_palvelu()

    #suoritetaan haku
    tulos = service.hae_nimea("testi")

    #ei pitäisis löytyä yhtään viitetta
    assert tulos == []

def test_hae_nimella_kun_ei_vastaavia_nimia():
    service= luo_palvelu()

    v1 = service.luo_viite(
        "book",
        {
            "author": "kirjoittaja",
            "title": "eiloydy",
            "year": "2000",
            "publisher": "Otava"
        })

    #suoritetaan haku
    tulos = service.hae_nimea("testi")

    #ei pitäisis löytyä yhtään viitetta
    assert tulos == []
    
def test_hae_kategoriaa_kun_kategoria_loytyy():
    service= luo_palvelu()

    #luodaan viitteita hakua varten
    v1 = service.luo_viite(
        "book",
        {
            "author": "kirjoittaja",
            "title": "tämmöne",
            "year": "2000",
            "publisher": "Otava",
            "category": "tärkeä"
        })

    v2 = service.luo_viite(
        "book",
        {
            "author": "kirjailija",
            "title": "tommonen",
            "year": "2001",
            "publisher": "WSOY",
            "category": "tärkeä"
        })
    
    v3 = service.luo_viite(
        "book",
        {
            "author": "kirjailija2",
            "title": "semmonen",
            "year": "2002",
            "publisher": "Otava",
            "category": "huono"
            
        })

    tulos = service.hae_kategoriaa("tärkeä")

    assert tulos == sorted([v1, v2], key=lambda v: v.tagit["category"].lower())
    
def test_hae_kategoriaa_kun_ei_ole_kategoriaa():
    service= luo_palvelu()

    tulos = service.hae_kategoriaa("tärkeä")

    assert tulos == []
    
def test_muokkaa_viitetta_kun_viite_olemassa():
    service= luo_palvelu()
    
    v1 = service.luo_viite(
        "book",
        {
            "author": "kirjoittaja",
            "title": "tämmöne",
            "year": "2000",
            "publisher": "Otava"
        })
    
    tulos = service.muokkaa_tagia("tämmöne", "year", "2020")
    assert tulos.tagit["year"] == "2020"
    
def test_muokkaa_viitetta_kun_viite_ei_ole_olemassa():
    service= luo_palvelu()
    
    tulos = service.muokkaa_tagia("tämmöne", "year", "2020")
    assert tulos == "Viitettä ei löytynyt."

def test_anna_viitteet():
    service= luo_palvelu()

    v1 = service.luo_viite(
        "book",
        {
            "author": "kirjoittaja",
            "title": "teos",
            "year": "2000",
            "publisher": "Otava"
        })

    v2 = service.luo_viite(
        "book",
        {
            "author": "kirjailija",
            "title": "teos2",
            "year": "2001",
            "publisher": "WSOY"
        })

    v3 = service.luo_viite(
        "article",
        {
            "author": "joku",
            "title": "testiartikkeli",
            "year": "2002",
            "publisher": "julkaisija"
        })

    tulos = service.anna_viitteet()
    assert tulos == sorted([v1, v2, v3],
        key=lambda v: (v.tyyppi.lower(), v.tagit.get("title", "").lower())
    )


# Suodata-testit

def test_suodata_tyypilla():
    service = luo_palvelu()
    
    service.luo_viite("book", {
        "author": "Kirjailija",
        "title": "Kirja1",
        "year": "2000",
        "publisher": "WSOY"
    })
    service.luo_viite("article", {
        "author": "Tutkija",
        "title": "Artikkeli1",
        "year": "2001",
        "journal": "Lehti"
    })
    
    tulokset = service.suodata(tyyppi="book")
    
    assert len(tulokset) == 1
    assert tulokset[0].tagit["title"] == "Kirja1"


def test_suodata_vuodella():
    service = luo_palvelu()
    
    service.luo_viite("book", {
        "author": "Kirjailija1",
        "title": "Kirja2000",
        "year": "2000",
        "publisher": "WSOY"
    })
    service.luo_viite("book", {
        "author": "Kirjailija2",
        "title": "Kirja2010",
        "year": "2010",
        "publisher": "Otava"
    })
    
    tulokset = service.suodata(vuosi="2000")
    
    assert len(tulokset) == 1
    assert tulokset[0].tagit["title"] == "Kirja2000"


def test_suodata_kirjoittajalla():
    service = luo_palvelu()
    
    service.luo_viite("book", {
        "author": "Mika Waltari",
        "title": "Sinuhe",
        "year": "1945",
        "publisher": "WSOY"
    })
    service.luo_viite("book", {
        "author": "Väinö Linna",
        "title": "Tuntematon",
        "year": "1954",
        "publisher": "WSOY"
    })
    
    tulokset = service.suodata(kirjoittaja="Waltari")
    
    assert len(tulokset) == 1
    assert tulokset[0].tagit["title"] == "Sinuhe"


def test_suodata_usealla_kriteerilla():
    service = luo_palvelu()
    
    service.luo_viite("book", {
        "author": "Mika Waltari",
        "title": "Sinuhe",
        "year": "1945",
        "publisher": "WSOY"
    })
    service.luo_viite("book", {
        "author": "Mika Waltari",
        "title": "Turms",
        "year": "1955",
        "publisher": "WSOY"
    })
    service.luo_viite("article", {
        "author": "Mika Waltari",
        "title": "Artikkeli",
        "year": "1945",
        "journal": "Lehti"
    })
    
    tulokset = service.suodata(tyyppi="book", vuosi="1945", kirjoittaja="Waltari")
    
    assert len(tulokset) == 1
    assert tulokset[0].tagit["title"] == "Sinuhe"


def test_suodata_ei_tuloksia():
    service = luo_palvelu()
    
    service.luo_viite("book", {
        "author": "Kirjailija",
        "title": "Kirja",
        "year": "2000",
        "publisher": "WSOY"
    })
    
    tulokset = service.suodata(vuosi="1999")
    
    assert len(tulokset) == 0


def test_suodata_ilman_kriteereja_palauttaa_kaikki():
    service = luo_palvelu()
    
    service.luo_viite("book", {
        "author": "Kirjailija1",
        "title": "Kirja1",
        "year": "2000",
        "publisher": "WSOY"
    })
    service.luo_viite("book", {
        "author": "Kirjailija2",
        "title": "Kirja2",
        "year": "2001",
        "publisher": "Otava"
    })
    
    tulokset = service.suodata()
    
    assert len(tulokset) == 2


# Viitteiden järjestäminen (sort) -testit

def test_anna_viitteet_jarjestaa_tyypin_mukaan():
    service = luo_palvelu()
    
    # Luodaan eri tyyppiset viitteet epäjärjestyksessä
    service.luo_viite("book", {
        "author": "Kirjailija",
        "title": "Zeta kirja",
        "year": "2000",
        "publisher": "WSOY"
    })
    service.luo_viite("article", {
        "author": "Tutkija",
        "title": "Alpha artikkeli",
        "year": "2001",
        "journal": "Lehti"
    })
    
    viitteet = service.anna_viitteet()
    
    # Article tulee ennen book (aakkosjärjestys)
    assert viitteet[0].tyyppi == "article"
    assert viitteet[1].tyyppi == "book"


def test_anna_viitteet_jarjestaa_nimen_mukaan_samassa_tyypissa():
    service = luo_palvelu()
    
    # Luodaan saman tyypin viitteet epäjärjestyksessä
    service.luo_viite("book", {
        "author": "Kirjailija1",
        "title": "Zeta",
        "year": "2000",
        "publisher": "WSOY"
    })
    service.luo_viite("book", {
        "author": "Kirjailija2",
        "title": "Alpha",
        "year": "2001",
        "publisher": "Otava"
    })
    service.luo_viite("book", {
        "author": "Kirjailija3",
        "title": "Beta",
        "year": "2002",
        "publisher": "WSOY"
    })
    
    viitteet = service.anna_viitteet()
    
    # Aakkosjärjestys nimen mukaan
    assert viitteet[0].tagit["title"] == "Alpha"
    assert viitteet[1].tagit["title"] == "Beta"
    assert viitteet[2].tagit["title"] == "Zeta"


def test_anna_viitteet_jarjestaa_isoilla_ja_pienilla_kirjaimilla():
    service = luo_palvelu()
    
    service.luo_viite("book", {
        "author": "Kirjailija1",
        "title": "alpha",
        "year": "2000",
        "publisher": "WSOY"
    })
    service.luo_viite("book", {
        "author": "Kirjailija2",
        "title": "BETA",
        "year": "2001",
        "publisher": "Otava"
    })
    
    viitteet = service.anna_viitteet()
    
    # Järjestys on case-insensitive
    assert viitteet[0].tagit["title"] == "alpha"
    assert viitteet[1].tagit["title"] == "BETA"


# anna_fi_nimi_ja_bib_nimi -testit

def test_anna_fi_nimi_ja_bib_nimi_suomeksi():
    service = luo_palvelu()
    
    (fi_nimi, bib_nimi) = service.anna_fi_nimi_ja_bib_nimi("kirjoittaja")
    
    assert fi_nimi == "kirjoittaja"
    assert bib_nimi == "author"


def test_anna_fi_nimi_ja_bib_nimi_englanniksi():
    service = luo_palvelu()
    
    (fi_nimi, bib_nimi) = service.anna_fi_nimi_ja_bib_nimi("author")
    
    assert fi_nimi == "kirjoittaja"
    assert bib_nimi == "author"


def test_anna_fi_nimi_ja_bib_nimi_tuntematon():
    service = luo_palvelu()
    
    (fi_nimi, bib_nimi) = service.anna_fi_nimi_ja_bib_nimi("tuntematon_tagi")
    
    assert fi_nimi is None
    assert bib_nimi is None
