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

