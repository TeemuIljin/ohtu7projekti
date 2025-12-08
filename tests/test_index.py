from unittest.mock import patch, MagicMock
from index import main


def test_main():
    """Test that main function creates App and calls run()."""
    with patch('index.ViiteRepository') as mock_repo_class, \
         patch('index.ViiteService') as mock_service_class, \
         patch('index.ConsoleIO') as mock_io_class, \
         patch('index.App') as mock_app_class:
        
        # Aseta mocks
        mock_repo_instance = MagicMock()
        mock_repo_class.return_value = mock_repo_instance
        
        mock_service_instance = MagicMock()
        mock_service_class.return_value = mock_service_instance
        
        mock_io_instance = MagicMock()
        mock_io_class.return_value = mock_io_instance
        
        mock_app_instance = MagicMock()
        mock_app_class.return_value = mock_app_instance
        
        
        main()
        
        # Varmistaa että App luodaan oikeilla argumenteilla
        mock_app_class.assert_called_once_with(mock_service_instance, mock_io_instance)
        # Tarkistaa että run kutsutaan app instanceen (line 12)
        mock_app_instance.run.assert_called_once()

