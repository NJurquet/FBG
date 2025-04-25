import os
import platform
if os.getenv("GITHUB_ACTIONS") == "true" or platform.system() == "Windows":
    from unittest.mock import MagicMock
    import sys
    sys.modules["RPLCD.i2c"] = MagicMock()
from RPLCD.i2c import CharLCD


class LCD:
    """
    Class to control a LCD 2004 (4 rows & 20 characters) display using I2C.
    """

    def __init__(self, address: int = 0x27):
        """
        Control a LCD display using I2C.

        Parameters:
            `address` (int, optional): The I2C address (in hexadecimal) of the LCD. Default is 0x27.
        """
        self._lcd = CharLCD(i2c_expander='PCF8574', address=address, port=1, cols=20, rows=4)
        self._lcd.clear()

    def write_line(self, row: int, message: str, line_feed: bool = True, carriage_return: bool = True) -> None:
        """
        Write a message to a specific row of the LCD display.

        Parameters:
            `row` (int): The row number (0-3) to write the message to.
            `message` (str): The message to display.
            `line_feed` (bool, optional): If True, fill the rest of the line with spaces. Default is True.
            `carriage_return` (bool, optional): If True, move the cursor to the beginning of the next line after writing the message. Default is True.

        Raises:
            `TypeError`: If the message is not a string or the row number is not an integer.
            `ValueError`: If the row number is not between 0 and 3.
        """
        if not isinstance(message, str):
            raise TypeError("LCD message must be a string")
        if not isinstance(row, int):
            raise TypeError("LCD row must be an integer")
        if row < 0 or row >= 4:
            raise ValueError("LCD row must be between 0 and 3")
        self._lcd.cursor_pos = (row, 0)
        self._lcd.write_string(message)
        if line_feed:
            self._lcd.lf()
        if carriage_return:
            self._lcd.cr()

    def write_score(self, score: int) -> None:
        """
        Write the score of the game to the LCD display.

        Parameters:
            `score` (int): The score to display.

        Raises:
            `TypeError`: If the score is not an integer.
            `ValueError`: If the score is negative.
        """
        if not isinstance(score, int):
            raise TypeError("LCD score must be an integer")
        if score < 0 or score > 120:
            raise ValueError("LCD score must be between 0 and 120")
        self._lcd.cursor_pos = (0, 0)
        self._lcd.write_string("FatBOTtommed Girls")
        self._lcd.lf()
        self._lcd.cursor_pos = (2, 0)
        self._lcd.write_string(f"Score: {score} points")

    def reset_cursor(self) -> None:
        """
        Reset the cursor position to the top left corner of the LCD display.
        """
        self._lcd.cursor_pos = (0, 0)

    def clear(self) -> None:
        """
        Clear the display by overwriting the data with blank characters and reset the cursor position.
        """
        self._lcd.clear()

    def close(self) -> None:
        self._lcd.close()
