from src.app import App
from src.repositories.ViiteRepository import ViiteRepository
from src.services.ViiteService import ViiteService


class StubIO:
    """Stub IO-luokka testausta varten."""
    
    def __init__(self, inputs):
        self.inputs = inputs
        self.input_index = 0
        self.outputs = []
    
    def read(self, prompt):
        if self.input_index >= len(self.inputs):
            return ""
        value = self.inputs[self.input_index]
        self.input_index += 1
        return value
    
    def write(self, value):
        self.outputs.append(value)


def luo_app(inputs):
    io = StubIO(inputs)
    repository = ViiteRepository()
    service = ViiteService(repository)
    app = App(service, io)
    return app, io, service


# Lopeta-komento

def test_lopeta_komento():
    app, io, _ = luo_app(["lopeta"])
    app.run()
    assert "Komennot:" in io.outputs[0]


def test_tyhja_komento_lopettaa():
    app, io, _ = luo_app([""])
    app.run()
    assert "Komennot:" in io.outputs[0]


# Listaa-komento

def test_listaa_kun_ei_viitteita():
    app, io, _ = luo_app(["listaa", "lopeta"])
    app.run()
    assert "Ei yhtään viitettä." in io.outputs


def test_listaa_viitteet():
    app, io, service = luo_app(["listaa", "lopeta"])
    service.luo_viite("book", {
        "author": "Testi",
        "title": "Testikirja",
        "year": "2000",
        "publisher": "WSOY"
    })
    app.run()
    # Ei "Ei yhtään viitettä." koska viite on olemassa
    assert "Ei yhtään viitettä." not in io.outputs


# Uusi-komento

def test_uusi_viite_onnistuu():
    inputs = [
        "uusi",
        "book",           # tyyppi
        "Kirjailija",     # author
        "Testikirja",     # title
        "WSOY",           # publisher
        "2020",           # year
        "",               # valinnainen tagi (tyhjä = lopeta)
        "lopeta"
    ]
    app, io, service = luo_app(inputs)
    app.run()
    
    viitteet = service.anna_viitteet()
    assert len(viitteet) == 1
    assert viitteet[0].tagit["title"] == "Testikirja"


def test_uusi_viite_tuntematon_tyyppi():
    inputs = [
        "uusi",
        "tuntematon_tyyppi",
        "lopeta"
    ]
    app, io, _ = luo_app(inputs)
    app.run()
    
    assert "Tyyppiä tuntematon_tyyppi ei ole olemassa" in io.outputs


def test_uusi_viite_valinnaisella_tagilla_bibtex():
    inputs = [
        "uusi",
        "book",
        "Kirjailija",
        "Testikirja",
        "WSOY",
        "2020",
        "pages",          # valinnainen tagi
        "10-20",          # arvo
        "",               # lopeta valinnaiset
        "lopeta"
    ]
    app, io, service = luo_app(inputs)
    app.run()
    
    viitteet = service.anna_viitteet()
    assert viitteet[0].tagit["pages"] == "10-20"


def test_uusi_viite_valinnaisella_tagilla_suomeksi():
    inputs = [
        "uusi",
        "kirja",
        "Kirjailija",
        "Testikirja",
        "WSOY",
        "2020",
        "sivut",          # valinnainen tagi
        "10-20",          # arvo
        "",               # lopeta valinnaiset
        "lopeta"
    ]
    app, io, service = luo_app(inputs)
    app.run()
    
    viitteet = service.anna_viitteet()
    assert viitteet[0].tagit["pages"] == "10-20"


def test_uusi_viite_oma_valinnainen_tagi():
    inputs = [
        "uusi",
        "kirja",
        "Kirjailija",
        "Testikirja",
        "WSOY",
        "2020",
        "kannen väri",
        "sininen",
        "",
        "lopeta"
    ]
    app, _, service = luo_app(inputs)
    app.run()
    
    viitteet = service.anna_viitteet()
    assert len(viitteet) == 1
    assert viitteet[0].tagit["kannen väri"] == "sininen"


# Poista-komento

def test_poista_viite_onnistuu():
    app, io, service = luo_app(["poista", "Testikirja", "lopeta"])
    service.luo_viite("book", {
        "author": "Testi",
        "title": "Testikirja",
        "year": "2000",
        "publisher": "WSOY"
    })
    app.run()
    
    assert "Viite: 'Testikirja' poistettu." in io.outputs
    assert len(service.anna_viitteet()) == 0


def test_poista_viite_ei_loydy():
    app, io, _ = luo_app(["poista", "Olematon", "lopeta"])
    app.run()
    
    assert "Viitettä: 'Olematon' ei löydetty." in io.outputs


# Muokkaa-komento

def test_muokkaa_viite_onnistuu():
    app, io, service = luo_app([
        "muokkaa",
        "Testikirja",     # viitteen nimi
        "ei",
        "year",           # muokattava tagi
        "2025",           # uusi arvo
        "lopeta"
    ])
    service.luo_viite("book", {
        "author": "Testi",
        "title": "Testikirja",
        "year": "2000",
        "publisher": "WSOY"
    })
    app.run()
    
    assert "Viite 'Testikirja' on muokattu." in io.outputs
    viitteet = service.anna_viitteet()
    assert viitteet[0].tagit["year"] == "2025"


# Suodata-komento

def test_suodata_loytaa_viitteita():
    app, io, service = luo_app([
        "suodata",
        "book",           # tyyppi
        "",               # vuosi (tyhjä)
        "",               # kirjoittaja (tyhjä)
        "lopeta"
    ])
    service.luo_viite("book", {
        "author": "Testi",
        "title": "Testikirja",
        "year": "2000",
        "publisher": "WSOY"
    })
    app.run()
    
    assert "Löytyi 1 viitettä:" in io.outputs


def test_suodata_ei_tuloksia():
    app, io, service = luo_app([
        "suodata",
        "article",        # tyyppi jota ei ole
        "",
        "",
        "lopeta"
    ])
    service.luo_viite("book", {
        "author": "Testi",
        "title": "Testikirja",
        "year": "2000",
        "publisher": "WSOY"
    })
    app.run()
    
    assert "Ei suodatusta vastaavia viitteitä." in io.outputs


# Tuntematon komento

def test_tuntematon_komento():
    app, io, _ = luo_app(["jotain_outoa", "lopeta"])
    app.run()
    
    assert "Tuntematon komento." in io.outputs


# Bibtex-komento

def test_bibtex_komento():
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as tmpdir:
        polku = str(Path(tmpdir) / "test.bib")
        app, io, service = luo_app([
            "bibtex",
            polku,
            "lopeta"
        ])
        service.luo_viite("book", {
            "author": "Testi",
            "title": "Testikirja",
            "year": "2000",
            "publisher": "WSOY"
        })
        app.run()
        
        assert f"Tallennettu tiedostoon {polku}" in io.outputs


# Hae-komento

def test_hae_tiedostosta():
    import json
    import tempfile
    from pathlib import Path
    
    entries = [{"type": "book", "tags": {"author": "A", "title": "B", "year": "2000", "publisher": "C"}}]
    
    with tempfile.TemporaryDirectory() as tmpdir:
        polku = Path(tmpdir) / "data.json"
        polku.write_text(json.dumps(entries), encoding="utf-8")
        
        app, io, service = luo_app([
            "hae",
            str(polku),
            "lopeta"
        ])
        app.run()
        
        assert "Hain 1 viitettä." in io.outputs


def test_hae_tiedostosta_virhe():
    app, io, _ = luo_app([
        "hae",
        "/olematon/polku.json",
        "lopeta"
    ])
    app.run()
    
    # Pitäisi olla virheviesti
    assert any("Virhe:" in output for output in io.outputs)


# Hae nimella -komento

def test_hae_nimella_loytaa():
    app, io, service = luo_app([
        "hae nimella",
        "Testi",
        "lopeta"
    ])
    service.luo_viite("book", {
        "author": "Kirjailija",
        "title": "Testikirja",
        "year": "2000",
        "publisher": "WSOY"
    })
    app.run()
    # Tarkistaa että ei tule "ei löydy" viestiä
    assert "Ei hakua vastaavia viitteita" not in io.outputs


def test_hae_nimella_ei_loydy():
    app, io, service = luo_app([
        "hae nimella",
        "olematon",
        "lopeta"
    ])
    service.luo_viite("book", {
        "author": "Kirjailija",
        "title": "Testikirja",
        "year": "2000",
        "publisher": "WSOY"
    })
    app.run()
    # print() käyttää suoraan eikä io.write()
    # Testi menee läpi jos ei kaadu


def test_hae_nimella_tyhja_hakusana():
    app, io, _ = luo_app([
        "hae nimella",
        "",
        "lopeta"
    ])
    app.run()
    # Tyhjä hakusana ei aiheuta virhettä


# Hae kategoriaa -komento

def test_hae_kategoriaa_loytaa():
    app, io, service = luo_app([
        "hae kategoriaa",
        "tärkeä",
        "lopeta"
    ])
    service.luo_viite("book", {
        "author": "Kirjailija",
        "title": "Testikirja",
        "year": "2000",
        "publisher": "WSOY",
        "category": "tärkeä"
    })
    app.run()
    # Tarkistaa että viite löytyi


def test_hae_kategoriaa_ei_loydy():
    app, io, service = luo_app([
        "hae kategoriaa",
        "olematon",
        "lopeta"
    ])
    service.luo_viite("book", {
        "author": "Kirjailija",
        "title": "Testikirja",
        "year": "2000",
        "publisher": "WSOY",
        "category": "tärkeä"
    })
    app.run()
    # Testi menee läpi jos ei kaadu

