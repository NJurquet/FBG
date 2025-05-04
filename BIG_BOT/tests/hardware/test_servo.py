import pytest
import sys
from unittest.mock import patch, MagicMock

# Mock the adafruit_servokit module BEFORE it's imported
sys.modules['adafruit_servokit'] = MagicMock()
# Create a mock ServoKit class that our code will use
mock_servo_kit = MagicMock()
sys.modules['adafruit_servokit'].ServoKit = mock_servo_kit

# Now it's safe to import the module that uses adafruit_servokit
from ...src.hardware.adafruitServoController import AdafruitServoControl

# Create a mock ServoKit class to avoid hardware dependencies
class MockServoKit:
    def __init__(self, channels):
        self.channels = channels
        self.servo = []
        # Create mock servos for each channel
        for i in range(channels):
            mock_servo = MagicMock()
            mock_servo.angle = None
            self.servo.append(mock_servo)

@pytest.fixture
def servo_control():
    # Patch the ServoKit class to use the mock implementation
    with patch('BIG_BOT.src.hardware.adafruitServoController.ServoKit', MockServoKit):
        # Create an actual AdafruitServoControl instance with mocked ServoKit
        names = ["servo1", "servo2", "outerRight", "outerLeft", 
                 "plankPusherRight", "plankPusherLeft", "hinge", "bannerDeployer"]
        pins = [0, 1, 2, 3, 4, 5, 6, 7]
        servo_control = AdafruitServoControl(channels=16, names=names, pins=pins)
        yield servo_control

class TestAdafruitServoControl:
    def test_servo_control_init(self):
        """Test that servo controller is initialized correctly"""
        with patch('BIG_BOT.src.hardware.adafruitServoController.ServoKit') as MockServoKit:
            names = ["servo1", "servo2"]
            pins = [0, 1]
            servo_control = AdafruitServoControl(channels=16, names=names, pins=pins)
            
            # We check that ServoKit was instantiated with correct channels
            MockServoKit.assert_called_once_with(channels=16)
            
            # We check that names and pins were stored correctly
            assert servo_control.names == names
            assert servo_control.pins == pins
            
            # We check that lastAngles was initialized with correct length
            assert len(servo_control.lastAngles) == len(names)
    
    def test_set_angles(self, servo_control):
        """Test that setAngles() method correctly sets angles for all servos"""
        angles = [30, 45, 60, 90, 120, 150, 180, 10]
        servo_control.setAngles(angles)
        
        # We check that angles were set correctly
        for i, angle in enumerate(angles):
            assert servo_control.kit.servo[i].angle == angle
            assert servo_control.lastAngles[i] == angle
    
    def test_set_outer_angles(self, servo_control):
        """Test that setOuterAngles() method correctly sets angles for outer servos"""
        angles = [60, 120]
        servo_control.setOuterAngles(angles)
        
        # We check that angles were set correctly for outer servos (index 2, 3)
        assert servo_control.kit.servo[2].angle == angles[0]
        assert servo_control.kit.servo[3].angle == angles[1]
        
        # We check that lastAngles was updated correctly
        assert servo_control.lastAngles[2] == angles[0]
        assert servo_control.lastAngles[3] == angles[1]
    
    def test_set_plank_pusher_angles(self, servo_control):
        """Test that setPlankPusherAngles() method correctly sets angles for plank pusher servos"""
        angles = [75, 105]
        servo_control.setPlankPusherAngles(angles)
        
        # We check that angles were set correctly for plank pusher servos (index 4, 5)
        assert servo_control.kit.servo[4].angle == angles[0]
        assert servo_control.kit.servo[5].angle == angles[1]
        
        # We check that lastAngles was updated correctly
        assert servo_control.lastAngles[4] == angles[0]
        assert servo_control.lastAngles[5] == angles[1]
    
    def test_set_banner_deployer_angle(self, servo_control):
        """Test that setBannerDeployerAngle() method correctly sets angle for banner deployer servo"""
        angle = 45
        servo_control.setBannerDeployerAngle(angle)
        
        # We check that angle was set correctly for banner deployer servo (index 7)
        assert servo_control.kit.servo[7].angle == angle
        
        # We check that lastAngles was updated correctly
        assert servo_control.lastAngles[7] == angle
    
    def test_stop_servo(self, servo_control):
        """Test that stopServo() method correctly stops specified servo"""
        channel = 3
        servo_control.stopServo(channel)
        
        # We check that angle was set to None to stop the servo
        assert servo_control.kit.servo[channel].angle is None
    
    def test_stop_servos(self, servo_control):
        """Test that stopServos() method correctly stops all servos"""
        servo_control.stopServos()
        
        # We check that all servos were stopped (angle set to None)
        for i in range(16):
            assert servo_control.kit.servo[i].angle is None
    
    def test_stop_outer_servos(self, servo_control):
        """Test that stopOuterServos() method correctly stops outer servos"""
        servo_control.stopOuterServos()
        
        # We check that outer servos (index 2, 3) were stopped (angle set to None)
        assert servo_control.kit.servo[2].angle is None
        assert servo_control.kit.servo[3].angle is None
    
    def test_set_angle_by_name(self, servo_control):
        """Test that setAngle() method correctly sets angle for specified servo by name"""
        name = "outerRight"  # Should correspond to index 2
        angle = 75
        servo_control.setAngle(name, angle)
        
        # We check that the angle was set correctly for the servo with specified name
        assert servo_control.kit.servo[2].angle == angle
    
    def test_compute_time_needed_all(self, servo_control):
        """Test computeTimeNeeded for all servos"""
        initial_angles = [10, 20, 30, 40, 50, 60, 70, 80]
        servo_control.setAngles(initial_angles)
        
        # New angles with biggest change of 50 degrees
        new_angles = [20, 30, 80, 40, 50, 60, 70, 80]
        time = servo_control.computeTimeNeeded(new_angles, "all")
        
        # With a _coef of 100, max angle diff 50 should give 0.5 seconds
        # But there's a minimum of 0.1 seconds
        expected_time = 50 / servo_control._coef
        assert time == max(expected_time, 0.1)
    
    def test_compute_time_needed_minimum(self, servo_control):
        """Test that computeTimeNeeded returns minimum time for small changes"""
        initial_angles = [10, 20, 30, 40, 50, 60, 70, 80]
        servo_control.setAngles(initial_angles)
        
        # New angles with small change
        new_angles = [11, 20, 30, 40, 50, 60, 70, 80]
        time = servo_control.computeTimeNeeded(new_angles, "all")
        
        # Should return minimum time
        assert time == 0.1