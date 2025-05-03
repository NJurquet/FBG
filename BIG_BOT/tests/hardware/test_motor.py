import pytest
from ...src.hardware.motorsControl import MotorsControl
from unittest.mock import patch

# Create a simple BigMotor mock class to avoid hardware dependencies
class MockBigMotor:
    def __init__(self, *args):
        self.forward_called = False
        self.backward_called = False
        self.stop_called = False
        self.forward_speed = 0
        self.backward_speed = 0
    
    def forward(self, speed):
        self.forward_called = True
        self.forward_speed = speed
    
    def backward(self, speed):
        self.backward_called = True
        self.backward_speed = speed
    
    def stop(self):
        self.stop_called = True
    
    def cleanup(self):
        self.cleanup_called = True

@pytest.fixture
def motors_control():
    # Patch the BigMotor class to use our mock implementation
    with patch('BIG_BOT.src.hardware.motorsControl.BigMotor', MockBigMotor):
        # Create an actual MotorsControl instance with our mocked BigMotor
        motors = MotorsControl(0, 1, 2, 3, 4, 5)
        yield motors

class TestMotorsControl:
    def test_motors_control_init(self):
        """Test that motors are initialized correctly during MotorsControl initialization"""
        with patch('BIG_BOT.src.hardware.motorsControl.BigMotor') as MockBigMotor:
            motors = MotorsControl(0, 1, 2, 3, 4, 5)
            
            # Check that BigMotor was instantiated twice (for left and right motors)
            assert MockBigMotor.call_count == 2
    
    def test_forward(self, motors_control):
        """Test that forward() method correctly calls forward() on both motors"""
        motors_control.forward(0.5)
        
        # Assert both motors' forward methods were called with the correct speed
        assert motors_control.leftMotor.forward_called == True
        assert motors_control.rightMotor.forward_called == True
        # Check speeds (allowing for offset adjustments)
        assert motors_control.leftMotor.forward_speed > 0
        assert motors_control.rightMotor.forward_speed > 0
    
    def test_backward(self, motors_control):
        """Test that backward() method correctly calls backward() on both motors"""
        motors_control.backward(0.5)
        
        # Assert both motors' backward methods were called
        assert motors_control.leftMotor.backward_called == True
        assert motors_control.rightMotor.backward_called == True
        # Check speeds (allowing for offset adjustments)
        assert motors_control.leftMotor.backward_speed > 0
        assert motors_control.rightMotor.backward_speed > 0
    
    def test_rotate_left(self, motors_control):
        """Test that rotateLeft() method correctly calls forward/backward with opposite directions"""
        motors_control.rotateLeft(0.5)
        
        # Assert correct motor directions were called
        assert motors_control.leftMotor.backward_called == True
        assert motors_control.rightMotor.forward_called == True
        # Check speeds (allowing for offset adjustments)
        assert motors_control.leftMotor.backward_speed > 0
        assert motors_control.rightMotor.forward_speed > 0
    
    def test_rotate_right(self, motors_control):
        """Test that rotateRight() method correctly calls forward/backward with opposite directions"""
        motors_control.rotateRight(0.5)
        
        # Assert correct motor directions were called
        assert motors_control.leftMotor.forward_called == True
        assert motors_control.rightMotor.backward_called == True
        # Check speeds (allowing for offset adjustments)
        assert motors_control.leftMotor.forward_speed > 0
        assert motors_control.rightMotor.backward_speed > 0
    
    def test_stop(self, motors_control):
        """Test that stop() method correctly calls stop() on both motors"""
        motors_control.stop()
        
        # Assert both motors' stop methods were called
        assert motors_control.leftMotor.stop_called == True
        assert motors_control.rightMotor.stop_called == True
        
    def test_cleanup(self, motors_control):
        """Test that cleanup() method correctly calls cleanup() on both motors"""
        motors_control.cleanup()
        
        # Assert both motors' cleanup methods were called
        assert motors_control.leftMotor.cleanup_called == True
        assert motors_control.rightMotor.cleanup_called == True
        
    def test_above_speed_limits(self, motors_control):
        """Test that speed is capped at a max of 1"""
        motors_control.forward(1.5)
        assert motors_control.leftMotor.forward_speed <= 1.0
        assert motors_control.rightMotor.forward_speed <= 1.0
        
        motors_control.backward(1.5)
        assert motors_control.leftMotor.backward_speed <= 1.0
        assert motors_control.rightMotor.backward_speed <= 1.0
        
        motors_control.rotateLeft(1.5)
        assert motors_control.leftMotor.backward_speed <= 1.0
        assert motors_control.rightMotor.forward_speed <= 1.0
        
        motors_control.rotateRight(1.5)
        assert motors_control.leftMotor.forward_speed <= 1.0
        assert motors_control.rightMotor.backward_speed <= 1.0
        
    def test_below_speed_limits(self, motors_control):
        """Test that speed is capped at a min of 0"""
        motors_control.forward(-0.5)
        assert motors_control.leftMotor.forward_speed >= 0.0
        assert motors_control.rightMotor.forward_speed >= 0.0
        
        motors_control.backward(-0.5)
        assert motors_control.leftMotor.backward_speed >= 0.0
        assert motors_control.rightMotor.backward_speed >= 0.0
        
        motors_control.rotateLeft(-0.5)
        assert motors_control.leftMotor.backward_speed >= 0.0
        assert motors_control.rightMotor.forward_speed >= 0.0
        
        motors_control.rotateRight(-0.5)
        assert motors_control.leftMotor.forward_speed >= 0.0
        assert motors_control.rightMotor.backward_speed >= 0.0