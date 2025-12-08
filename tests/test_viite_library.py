import pytest
from repositories.ViiteRepository import ViiteRepository
from services.ViiteService import ViiteService
from ViiteLibrary import ViiteLibrary


def test_viitetta_ei_loydy_listalta_kun_viite_loytyy():
    """Test that viitetta_ei_loydy_listalta raises AssertionError when viite is found."""
    library = ViiteLibrary()
    
    # luo viite ensin
    library.luo_viite("book", "Test Author", "Test Book", "2020", "Test Publisher")
    
    # Löytyykö se
    with pytest.raises(AssertionError, match="Viite 'Test Book' löytyy vielä listalta"):
        library.viitetta_ei_loydy_listalta("Test Book")

