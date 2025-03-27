import pytest
from unittest.mock import Mock
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

    def test_add_sensor(self, controller: UltrasonicController):
        Device.pin_factory = MockFactory()

        controller.add_sensor(USPosition.FRONT_RIGHT, 1, 2)

        assert any(sensor.pos == USPosition.FRONT_RIGHT for sensor in controller._sensors)
        assert len(controller._sensors) == 1

        with pytest.raises(ValueError):
            controller.add_sensor(USPosition.FRONT_RIGHT, 3, 4)

    def test_check_obstacles_no_event(self, controller: UltrasonicController):
        sensor1 = Mock(spec=UltrasonicSensor)
        sensor1.pos = USPosition.FRONT_RIGHT
        sensor1.getDistance.return_value = 45.3
        sensor2 = Mock(spec=UltrasonicSensor)
        sensor2.pos = USPosition.FRONT_LEFT
        sensor2.getDistance.return_value = 80.0

        controller._sensors = [sensor1, sensor2]

        controller.measure_distances()
        assert controller.check_obstacles() == USEvent.NO_EVENT
        # Sensors present with no distances
        controller._distances = {}
        assert controller.check_obstacles() == USEvent.NO_EVENT
        # No sensors present with distances
        controller._sensors = []
        controller.measure_distances()
        assert controller.check_obstacles() == USEvent.NO_EVENT
        # No sensors present with no distances
        controller._distances = {}
        assert controller.check_obstacles() == USEvent.NO_EVENT

    @pytest.mark.skip("Not implemented")
    def test_check_obstacles_obstacle_detected(self):
        pass

    @pytest.mark.skip("Not implemented")
    def test_check_obstacles_obstacle_cleared(self):
        pass

    @pytest.mark.skip("Not implemented")
    def test_measure_distances(self):
        pass

    @pytest.mark.skip("Not implemented")
    def test_get_distance(self):
        pass
