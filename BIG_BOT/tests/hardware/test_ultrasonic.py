import pytest
from unittest.mock import Mock, patch
from time import sleep, perf_counter

from ...src.hardware.ultrasonicController import UltrasonicController
from ...src.hardware.ultrasonicSensor import UltrasonicSensor
from ...src.constants import USPosition, USEvent

from gpiozero import Device
from gpiozero.pins.mock import MockFactory, MockTriggerPin


class PreciseMockTriggerPin(MockTriggerPin):
    def _echo(self):
        if self.echo_pin is None:
            raise ValueError("echo_pin is not initialized")

        sleep(0.001)
        self.echo_pin.drive_high()

        # sleep(), time() and monotonic() dont have enough precision!
        init_time = perf_counter()
        while True:
            if perf_counter() - init_time >= self.echo_time:
                break

        self.echo_pin.drive_low()


@pytest.fixture
def controller():
    return UltrasonicController()


class TestUltrasonicController:
    def test_init(self, controller: UltrasonicController):
        assert controller._sensors == []
        assert controller._distances == {}
        assert controller._last_obstacle is False
        assert controller._enabled_sensors == {}

    @patch('BIG_BOT.src.hardware.ultrasonicController.UltrasonicSensor')
    def test_add_sensor(self, mock_sensor_class, controller: UltrasonicController):
        # Setup mock sensor instance
        mock_sensor = Mock()
        mock_sensor.pos = USPosition.FRONT_RIGHT
        mock_sensor.echoPin = 1
        mock_sensor.trigPin = 2
        mock_sensor_class.return_value = mock_sensor

        controller.add_sensor(USPosition.FRONT_RIGHT, 1, 2)

        # Verify UltrasonicSensor was created with correct parameters
        mock_sensor_class.assert_called_once_with(USPosition.FRONT_RIGHT, 1, 2)
        
        assert len(controller._sensors) == 1
        assert controller._sensors[0] == mock_sensor
        assert controller._enabled_sensors[USPosition.FRONT_RIGHT] is True

        with pytest.raises(ValueError):
            controller.add_sensor(USPosition.FRONT_RIGHT, 3, 4)
        with pytest.raises(TypeError):
            controller.add_sensor("invalid position type", 1, 2)  # type: ignore
        with pytest.raises(TypeError):
            controller.add_sensor(USPosition.FRONT_RIGHT, "1", "2")  # type: ignore
        with pytest.raises(ValueError):
            controller.add_sensor(USPosition.FRONT_RIGHT, -1, -2)
        with pytest.raises(ValueError):
            controller.add_sensor(USPosition.FRONT_RIGHT, 3, 3)

    def test_enable_disable_toggle_sensor(self, controller: UltrasonicController):
        # Directly setup the controller's internal state
        controller._enabled_sensors[USPosition.FRONT_RIGHT] = True
        
        # Test disable
        controller.disable_sensor(USPosition.FRONT_RIGHT)
        assert controller._enabled_sensors[USPosition.FRONT_RIGHT] is False
        
        # Test enable
        controller.enable_sensor(USPosition.FRONT_RIGHT)
        assert controller._enabled_sensors[USPosition.FRONT_RIGHT] is True
        
        # Test toggle (from True to False)
        controller.toggle_sensor(USPosition.FRONT_RIGHT)
        assert controller._enabled_sensors[USPosition.FRONT_RIGHT] is False
        
        # Test toggle (from False to True)
        controller.toggle_sensor(USPosition.FRONT_RIGHT)
        assert controller._enabled_sensors[USPosition.FRONT_RIGHT] is True
        
        # Test with nonexistent sensor position
        controller.disable_sensor(USPosition.FRONT_LEFT)  # Should just print a message, not raise exception
        controller.enable_sensor(USPosition.FRONT_LEFT)   # Should just print a message, not raise exception
        controller.toggle_sensor(USPosition.FRONT_LEFT)   # Should just print a message, not raise exception

    def test_get_enabled_sensors(self, controller: UltrasonicController):
        # Directly setup the controller's internal state
        controller._enabled_sensors = {
            USPosition.FRONT_RIGHT: True,
            USPosition.FRONT_LEFT: True
        }
        
        enabled_sensors = controller.get_enabled_sensors()
        assert enabled_sensors[USPosition.FRONT_RIGHT] is True
        assert enabled_sensors[USPosition.FRONT_LEFT] is True
        
        controller.disable_sensor(USPosition.FRONT_LEFT)
        enabled_sensors = controller.get_enabled_sensors()
        assert enabled_sensors[USPosition.FRONT_RIGHT] is True
        assert enabled_sensors[USPosition.FRONT_LEFT] is False

    def test_check_obstacles_no_event(self, controller: UltrasonicController):
        sensor1 = Mock(spec=UltrasonicSensor)
        sensor1.pos = USPosition.FRONT_RIGHT
        sensor2 = Mock(spec=UltrasonicSensor)
        sensor2.pos = USPosition.FRONT_LEFT

        sensors: list[UltrasonicSensor] = [sensor1, sensor2]
        distances: dict[USPosition, float] = {
            USPosition.FRONT_RIGHT: 45.0,
            USPosition.FRONT_LEFT: 80.0,
        }
        controller._sensors = sensors
        controller._distances = distances
        controller._enabled_sensors = {
            USPosition.FRONT_RIGHT: True,
            USPosition.FRONT_LEFT: True
        }

        assert controller.check_obstacles() == USEvent.NO_EVENT
        # Sensors present with no distances
        controller._distances = {}
        assert controller.check_obstacles() == USEvent.NO_EVENT
        # No sensors present with distances
        controller._sensors = []
        controller._distances = distances
        assert controller.check_obstacles() == USEvent.NO_EVENT
        # No sensors present with no distances
        controller._distances = {}
        assert controller.check_obstacles() == USEvent.NO_EVENT

    def test_check_obstacles_obstacle_detected_present(self, controller: UltrasonicController):
        sensor1 = Mock(spec=UltrasonicSensor)
        sensor1.pos = USPosition.FRONT_RIGHT
        sensor2 = Mock(spec=UltrasonicSensor)
        sensor2.pos = USPosition.FRONT_LEFT

        sensors: list[UltrasonicSensor] = [sensor1, sensor2]
        distances: dict[USPosition, float] = {
            USPosition.FRONT_RIGHT: 5.0,
            USPosition.FRONT_LEFT: 80.0,
        }
        controller._sensors = sensors
        controller._distances = distances
        controller._enabled_sensors = {
            USPosition.FRONT_RIGHT: True,
            USPosition.FRONT_LEFT: True
        }

        assert controller.check_obstacles() == USEvent.OBSTACLE_DETECTED
        assert controller._last_obstacle is True
        assert controller.check_obstacles() == USEvent.OBSTACLE_PRESENT
        assert controller._last_obstacle is True

    def test_check_obstacles_disabled_sensor(self, controller: UltrasonicController):
        sensor1 = Mock(spec=UltrasonicSensor)
        sensor1.pos = USPosition.FRONT_RIGHT
        sensor2 = Mock(spec=UltrasonicSensor)
        sensor2.pos = USPosition.FRONT_LEFT

        sensors: list[UltrasonicSensor] = [sensor1, sensor2]
        distances: dict[USPosition, float] = {
            USPosition.FRONT_RIGHT: 5.0,  # Would trigger obstacle if enabled
            USPosition.FRONT_LEFT: 80.0,
        }
        controller._sensors = sensors
        controller._distances = distances
        controller._enabled_sensors = {
            USPosition.FRONT_RIGHT: False,  # Disabled sensor with obstacle
            USPosition.FRONT_LEFT: True
        }

        # Should return NO_EVENT since the sensor with obstacle is disabled
        assert controller.check_obstacles() == USEvent.NO_EVENT
        assert controller._last_obstacle is False

    def test_check_obstacles_obstacle_cleared(self, controller: UltrasonicController):
        sensor1 = Mock(spec=UltrasonicSensor)
        sensor1.pos = USPosition.FRONT_RIGHT
        sensor2 = Mock(spec=UltrasonicSensor)
        sensor2.pos = USPosition.FRONT_LEFT

        sensors: list[UltrasonicSensor] = [sensor1, sensor2]
        distances: dict[USPosition, float] = {
            USPosition.FRONT_RIGHT: 45.0,
            USPosition.FRONT_LEFT: 80.0,
        }
        controller._sensors = sensors
        controller._distances = distances
        controller._enabled_sensors = {
            USPosition.FRONT_RIGHT: True,
            USPosition.FRONT_LEFT: True
        }
        controller._last_obstacle = True

        assert controller.check_obstacles() == USEvent.OBSTACLE_CLEARED
        assert controller._last_obstacle is False

    def test_measure_distances(self, controller: UltrasonicController):
        sensor1 = Mock(spec=UltrasonicSensor)
        sensor1.pos = USPosition.FRONT_RIGHT
        sensor1.getDistance.return_value = 45.3
        sensor2 = Mock(spec=UltrasonicSensor)
        sensor2.pos = USPosition.FRONT_LEFT
        sensor2.getDistance.return_value = 80.0
        controller._sensors = [sensor1, sensor2]
        controller._enabled_sensors = {
            USPosition.FRONT_RIGHT: True,
            USPosition.FRONT_LEFT: True
        }

        controller.measure_distances()
        assert len(controller._distances) == 2
        assert controller._distances[sensor1.pos] == 45.3
        assert controller._distances[sensor2.pos] == 80.0
        
        # Test with one disabled sensor
        controller._enabled_sensors[USPosition.FRONT_LEFT] = False
        controller.measure_distances()
        assert len(controller._distances) == 1
        assert controller._distances[sensor1.pos] == 45.3
        assert USPosition.FRONT_LEFT not in controller._distances

    @patch('BIG_BOT.src.hardware.ultrasonicController.UltrasonicSensor')
    def test_get_distance_valid_position(self, mock_sensor_class, controller: UltrasonicController):
        # Create mock sensor
        mock_sensor = Mock(spec=UltrasonicSensor)
        mock_sensor.pos = USPosition.FRONT_RIGHT
        mock_sensor.getDistance.return_value = 45.0
        
        # Setup controller directly
        controller._sensors = [mock_sensor]
        controller._enabled_sensors = {USPosition.FRONT_RIGHT: True}

        distance = controller.get_distance(USPosition.FRONT_RIGHT)
        assert distance == 45.0
        mock_sensor.getDistance.assert_called_once()

    def test_get_distance_invalid_position(self, controller: UltrasonicController):
        with pytest.raises(TypeError):
            controller.get_distance("invalid position type")  # type: ignore
        with pytest.raises(ValueError):
            controller.get_distance(USPosition.FRONT_RIGHT)