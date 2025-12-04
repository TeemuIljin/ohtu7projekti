from repositories.ViiteRepository import ViiteRepository
from services.ViiteService import ViiteService


class ViiteLibrary:
    """Robot Framework -kirjasto viitteiden testaukseen."""

    def __init__(self):
        self._repository = ViiteRepository()
        self._service = ViiteService(self._repository)

    def luo_viite(self, tyyppi, kirjoittaja, nimi, vuosi, julkaisija=None):
        """Luo uuden viitteen annetuilla tiedoilla."""
        tagit = {
            "author": kirjoittaja,
            "title": nimi,
            "year": vuosi
        }
        if julkaisija:
            tagit["publisher"] = julkaisija

        self._service.luo_viite(tyyppi, tagit)

    def viitteiden_maara_on(self, odotettu):
        """Tarkistaa, että viitteiden määrä on odotettu."""
        viitteet = self._service.anna_viitteet()
        odotettu_int = int(odotettu)

        if len(viitteet) != odotettu_int:
            raise AssertionError(
                f"Viitteiden määrä {len(viitteet)} != odotettu {odotettu_int}"
            )

    def listaa_viitteet(self):
        """Palauttaa kaikki viitteet."""
        return self._service.anna_viitteet()

    def viite_loytyyy_listalta(self, nimi):
        """Tarkistaa, että viite löytyy listalta nimen perusteella."""
        viitteet = self._service.anna_viitteet()

        for viite in viitteet:
            if viite.tagit.get("title") == nimi:
                return True

        raise AssertionError(f"Viitettä '{nimi}' ei löydy listalta")

    def viitetta_ei_loydy_listalta(self, nimi):
        """Tarkistaa, että viitettä EI löydy listalta."""
        viitteet = self._service.anna_viitteet()

        for viite in viitteet:
            if viite.tagit.get("title") == nimi:
                raise AssertionError(f"Viite '{nimi}' löytyy vielä listalta")

        return True

    def poista_viite(self, nimi):
        """Poistaa viitteen nimen perusteella."""
        return self._service.poista_viite(nimi)

    def poisto_onnistui(self, tulos):
        """Tarkistaa, että poisto onnistui."""
        if not tulos:
            raise AssertionError("Viitteen poisto epäonnistui")

    def poisto_epaonnistui(self, tulos):
        """Tarkistaa, että poisto epäonnistui (viitettä ei löytynyt)."""
        if tulos:
            raise AssertionError("Viitteen poiston piti epäonnistua")

    def suodata_tyypilla(self, tyyppi):
        """Suodattaa viitteet tyypin perusteella."""
        return self._service.suodata(tyyppi=tyyppi)

    def suodata_vuodella(self, vuosi):
        """Suodattaa viitteet vuoden perusteella."""
        return self._service.suodata(vuosi=vuosi)

    def suodata_kirjoittajalla(self, kirjoittaja):
        """Suodattaa viitteet kirjoittajan perusteella."""
        return self._service.suodata(kirjoittaja=kirjoittaja)

    def suodatettujen_maara_on(self, tulokset, odotettu):
        """Tarkistaa suodatettujen viitteiden määrän."""
        odotettu_int = int(odotettu)

        if len(tulokset) != odotettu_int:
            raise AssertionError(
                f"Suodatettujen määrä {len(tulokset)} != odotettu {odotettu_int}"
            )

    def suodatetuissa_on_viite(self, tulokset, nimi):
        """Tarkistaa, että suodatetuissa on tietty viite."""
        for viite in tulokset:
            if viite.tagit.get("title") == nimi:
                return True

        raise AssertionError(f"Viitettä '{nimi}' ei löydy suodatetuista")

