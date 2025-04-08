import pytest
from ...src.hardware.lcd import LCD


@pytest.fixture
def lcd() -> LCD:
    return LCD()


class TestLCD:
    def test_init(self, lcd: LCD):
        assert lcd._lcd is not None

    def test_write_line_valid(self, lcd: LCD):
        assert lcd.write_line(0, "Hello World") is None
        assert lcd.write_line(1, "Test Message", line_feed=False) is None
        assert lcd.write_line(2, "Another Test", carriage_return=False) is None
        assert lcd.write_line(3, "Final Test", line_feed=False, carriage_return=False) is None

    def test_write_line_invalid(self, lcd: LCD):
        with pytest.raises(ValueError):
            lcd.write_line(4, "Invalid Row")

        with pytest.raises(TypeError):
            lcd.write_line("0", "Invalid row type")  # type: ignore

        with pytest.raises(TypeError):
            lcd.write_line(0, 12345)  # type: ignore

    def test_write_score(self, lcd: LCD):
        with pytest.raises(TypeError):
            lcd.write_score("100")  # type: ignore

        with pytest.raises(ValueError):
            lcd.write_score(-10)

        with pytest.raises(ValueError):
            lcd.write_score(150)

        assert lcd.write_score(100) is None

    def test_clear(self, lcd: LCD):
        assert lcd.clear() is None

    def test_close(self, lcd: LCD):
        assert lcd.close() is None
