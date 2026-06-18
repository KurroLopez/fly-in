
from map import Map


class Process:
    __turn: int
    __map: Map

    def __init__(self, map: Map):
        """
        Initialize the Process with a given Map.
        """
        self.__map = map
        self.__turn = 0

    @property
    def turn(self) -> int:
        """
        Get the current turn number.

        return:
            int: The current turn number.
        """
        return self.__turn

    def reset(self):
        """
        Reset the process to its initial state.
        """
        self.__turn = 0

    def next(self):
        """
        Move to the next step in the process.
        """
        self.__turn += 1
