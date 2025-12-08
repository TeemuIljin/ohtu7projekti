from unittest.mock import patch
from ConsoleIO import ConsoleIO


def test_console_io_read():
    """Test that ConsoleIO.read calls input with the prompt."""
    console_io = ConsoleIO()
    
    with patch('builtins.input', return_value='test input') as mock_input:
        result = console_io.read("Enter something: ")
        
        mock_input.assert_called_once_with("Enter something: ")
        assert result == 'test input'

