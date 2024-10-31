import pygetwindow as gw


class Window:
    def __init__(self, name):
        self._name = name
        self.__window = gw.getWindowsWithTitle(self._name)[0]

    def close_window(self):
        self.__window.close()
        
