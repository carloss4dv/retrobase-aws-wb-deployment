import pygetwindow as gw
from PIL import Image
import pytesseract as pt
import pyautogui
import os
import time


class Window:

    def __init__(self, name):
        self._name = name
        self.__window = gw.getWindowsWithTitle(self._name)[0]
        self.__coor = [self.__window.left, self.__window.top,
                       self.__window.width, self.__window.height]

    def __relocate_window_size(self):
        self.__window.moveTo(100, 100)

        self.__coor[0], self.__coor[1] = 100, 100

        w = 100+self.__window.width
        h = 100+self.__window.height

        self.__coor[2], self.__coor[3] = w, h

        return [100, 100, w, h]

    def __window_screenshot(self, fullscreen=False):
        # Define las coordenadas de la zona que deseas capturar
        if (fullscreen):
            x1, y1, x2, y2 = 0, 0, self.__window.width, self.__window.height
        else:
            # Define las coordenadas izquierda arriba y derecha abajo
            x1, y1, x2, y2 = self.__coor[0]+3, self.__coor[1]+25, self.__coor[2]-2, self.__coor[3]

        # Captura la zona de la pantalla
        # captura = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        screenshot = pyautogui.screenshot(region=(x1, y1, x2, y2))

        # Guarda la captura en un archivo de imagen
        screenshot.save("screenshot.png")

        # Cierra la captura
        screenshot.close()

    def __read_image(self):
        image = Image.open('screenshot.png')
        string = pt.image_to_string(image, lang="spa", config='--psm 6')
        # string = pt.image_to_string(imagen, lang="spa")
        return string

    def __delete_image(self):
        file_to_delete = "screenshot.png"
        if os.path.exists(file_to_delete):
            os.remove(file_to_delete)

    def __remove_null_lines(self, string):
        # Divide el texto en líneas y filtra las líneas no vacías
        lines = [line for line in string.splitlines() if line.strip()]

        # Une las líneas en un solo string nuevamente
        cleaned_string = '\n'.join(lines)

        return cleaned_string

    def __window_info(self):
        self.__relocate_window_size()
        self.__window_screenshot()
        time.sleep(4)
        image = self.__read_image()
        # self.__delete_imagen()
        return image

    def __info_full_window(self):
        self.__window_screenshot(fullscreen=True)
        time.sleep(4)
        image = self.__read_image()
        # self.__delete_imagen()
        return image

    def print(self):
        print(self.__window)
        print(self._name)
        print(self.__coor)

    def close_window(self):
        self.__window.close()
