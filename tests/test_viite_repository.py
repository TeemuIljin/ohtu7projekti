from src.repositories.ViiteRepository import ViiteRepository

class RandomMock:
    def choices(self, k):
        return list("sattumanvarainen123")


def luo_kokoelma():
    return ViiteRepository(RandomMock)


def test_anna_vapaa_viite_id():
    kokoelma = luo_kokoelma()

    viite_id = kokoelma.anna_vapaa_viite_id("", "")
    assert viite_id == "sattumanvarainen123"

    viite_id = kokoelma.anna_vapaa_viite_id("Kirjoittaja", "")
    assert viite_id == "sattumanvarainen123"

    viite_id = kokoelma.anna_vapaa_viite_id("", "Vuosi")
    assert viite_id == "sattumanvarainen123"

    viite_id = kokoelma.anna_vapaa_viite_id("Kirjoittaja", "Vuosi")
    assert viite_id == "KirjoittajaVuosi"
