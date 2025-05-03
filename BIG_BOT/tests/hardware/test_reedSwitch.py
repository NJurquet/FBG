import pytest
import sys
from unittest.mock import patch, MagicMock

# Mock the gpiozero module before it's imported
sys.modules['gpiozero'] = MagicMock()
mock_button = MagicMock()
sys.modules['gpiozero'].Button = mock_button

# Now it's safe to import the module that uses gpiozero
from ...src.hardware.reedSwitch import reedSwitch

# Create a MockButton class to simulate reed switch behavior
class MockButton:
    def __init__(self, pin, pull_up=None):
        self.pin = pin
        self.pull_up = pull_up
        self._is_pressed = False
    
    @property
    def is_pressed(self):
        return self._is_pressed
    
    def set_pressed(self, value):
        self._is_pressed = value

@pytest.fixture
def reed_switch():
    # Patch the Button class to use our mock implementation
    with patch('BIG_BOT.src.hardware.reedSwitch.Button', MockButton):
        # Create an actual reedSwitch instance with mocked Button
        reed = reedSwitch(pin=17)
        yield reed

class TestReedSwitch:
    def test_reed_switch_init(self):
        """Test that reed switch is initialized correctly"""
        with patch('BIG_BOT.src.hardware.reedSwitch.Button') as MockButton:
            reed = reedSwitch(pin=17)
            
            # Check that Button was instantiated with correct parameters
            MockButton.assert_called_once_with(17, pull_up=False)
    
    def test_read_not_pressed(self, reed_switch):
        """Test read() method when reed switch is not pressed"""
        # Set the mock button to not pressed
        reed_switch.reedSwitch._is_pressed = False
        
        # Check that read() returns False
        assert reed_switch.read() == False
    
    def test_read_pressed(self, reed_switch):
        """Test read() method when reed switch is pressed"""
        # Set the mock button to pressed
        reed_switch.reedSwitch._is_pressed = True
        
        # Check that read() returns True
        assert reed_switch.read() == True