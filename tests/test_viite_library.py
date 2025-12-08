import pytest
from repositories.ViiteRepository import ViiteRepository
from services.ViiteService import ViiteService
from ViiteLibrary import ViiteLibrary


def test_viite_library_init():
    """Test that ViiteLibrary initializes correctly."""
    library = ViiteLibrary()
    assert library._repository is not None
    assert library._service is not None


def test_luo_viite_with_publisher():
    """Test luo_viite with publisher."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author", "Title", "2020", "Publisher")
    viitteet = library.listaa_viitteet()
    assert len(viitteet) == 1
    assert viitteet[0].tagit.get("publisher") == "Publisher"


def test_luo_viite_without_publisher():
    """Test luo_viite without publisher."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author", "Title", "2020")
    viitteet = library.listaa_viitteet()
    assert len(viitteet) == 1
    assert "publisher" not in viitteet[0].tagit


def test_viitteiden_maara_on_success():
    """Test viitteiden_maara_on when count matches."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author", "Title", "2020")
    library.viitteiden_maara_on("1")  # Should not raise


def test_viitteiden_maara_on_failure():
    """Test viitteiden_maara_on when count doesn't match."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author", "Title", "2020")
    with pytest.raises(AssertionError, match="Viitteiden määrä 1 != odotettu 2"):
        library.viitteiden_maara_on("2")


def test_listaa_viitteet():
    """Test listaa_viitteet returns all viitteet."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author1", "Title1", "2020")
    library.luo_viite("article", "Author2", "Title2", "2021")
    viitteet = library.listaa_viitteet()
    assert len(viitteet) == 2


def test_viite_loytyyy_listalta_success():
    """Test viite_loytyyy_listalta when viite is found."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author", "Test Book", "2020")
    result = library.viite_loytyyy_listalta("Test Book")
    assert result is True


def test_viite_loytyyy_listalta_failure():
    """Test viite_loytyyy_listalta when viite is not found."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author", "Other Book", "2020")
    with pytest.raises(AssertionError, match="Viitettä 'Test Book' ei löydy listalta"):
        library.viite_loytyyy_listalta("Test Book")


def test_viitetta_ei_loydy_listalta_kun_viite_loytyy():
    """Test that viitetta_ei_loydy_listalta raises AssertionError when viite is found."""
    library = ViiteLibrary()
    
    # luo viite ensin
    library.luo_viite("book", "Test Author", "Test Book", "2020", "Test Publisher")
    
    # Löytyykö se
    with pytest.raises(AssertionError, match="Viite 'Test Book' löytyy vielä listalta"):
        library.viitetta_ei_loydy_listalta("Test Book")


def test_viitetta_ei_loydy_listalta_kun_viitetta_ei_loydy():
    """Test viitetta_ei_loydy_listalta when viite is not found."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author", "Other Book", "2020")
    result = library.viitetta_ei_loydy_listalta("Test Book")
    assert result is True


def test_poista_viite():
    """Test poista_viite."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author", "Test Book", "2020")
    result = library.poista_viite("Test Book")
    assert result is True
    library.viitteiden_maara_on("0")


def test_poisto_onnistui_success():
    """Test poisto_onnistui when result is True."""
    library = ViiteLibrary()
    library.poisto_onnistui(True)  # Should not raise


def test_poisto_onnistui_failure():
    """Test poisto_onnistui when result is False."""
    library = ViiteLibrary()
    with pytest.raises(AssertionError, match="Viitteen poisto epäonnistui"):
        library.poisto_onnistui(False)


def test_poisto_epaonnistui_success():
    """Test poisto_epaonnistui when result is False."""
    library = ViiteLibrary()
    library.poisto_epaonnistui(False)  # Should not raise


def test_poisto_epaonnistui_failure():
    """Test poisto_epaonnistui when result is True."""
    library = ViiteLibrary()
    with pytest.raises(AssertionError, match="Viitteen poiston piti epäonnistua"):
        library.poisto_epaonnistui(True)


def test_suodata_tyypilla():
    """Test suodata_tyypilla."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author1", "Book1", "2020")
    library.luo_viite("article", "Author2", "Article1", "2020")
    tulokset = library.suodata_tyypilla("book")
    assert len(tulokset) == 1
    assert tulokset[0].tyyppi == "book"


def test_suodata_vuodella():
    """Test suodata_vuodella."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author1", "Book1", "2020")
    library.luo_viite("book", "Author2", "Book2", "2021")
    tulokset = library.suodata_vuodella("2020")
    assert len(tulokset) == 1
    assert tulokset[0].tagit.get("year") == "2020"


def test_suodata_kirjoittajalla():
    """Test suodata_kirjoittajalla."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author1", "Book1", "2020")
    library.luo_viite("book", "Author2", "Book2", "2021")
    tulokset = library.suodata_kirjoittajalla("Author1")
    assert len(tulokset) == 1
    assert tulokset[0].tagit.get("author") == "Author1"


def test_suodatettujen_maara_on_success():
    """Test suodatettujen_maara_on when count matches."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author", "Book1", "2020")
    library.luo_viite("book", "Author", "Book2", "2020")
    tulokset = library.suodata_tyypilla("book")
    library.suodatettujen_maara_on(tulokset, "2")  # Should not raise


def test_suodatettujen_maara_on_failure():
    """Test suodatettujen_maara_on when count doesn't match."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author", "Book1", "2020")
    tulokset = library.suodata_tyypilla("book")
    with pytest.raises(AssertionError, match="Suodatettujen määrä 1 != odotettu 2"):
        library.suodatettujen_maara_on(tulokset, "2")


def test_suodatetuissa_on_viite_success():
    """Test suodatetuissa_on_viite when viite is found."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author", "Test Book", "2020")
    tulokset = library.suodata_tyypilla("book")
    result = library.suodatetuissa_on_viite(tulokset, "Test Book")
    assert result is True


def test_suodatetuissa_on_viite_failure():
    """Test suodatetuissa_on_viite when viite is not found."""
    library = ViiteLibrary()
    library.luo_viite("book", "Author", "Other Book", "2020")
    tulokset = library.suodata_tyypilla("book")
    with pytest.raises(AssertionError, match="Viitettä 'Test Book' ei löydy suodatetuista"):
        library.suodatetuissa_on_viite(tulokset, "Test Book")

