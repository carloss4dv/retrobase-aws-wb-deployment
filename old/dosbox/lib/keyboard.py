from pynput.keyboard import Key, Controller

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Keyboard(metaclass=Singleton):
    def __init__(self):
        self.__keyboard = Controller()

    def press(self, key):
        key = key.lower()
        if key == ' ':
            self.__keyboard.press(Key.space)
            self.__keyboard.release(Key.space)
        else:
            if key.isalpha():
                self.__keyboard.press(Key.shift)
                self.__keyboard.press(key)
                self.__keyboard.release(key)
                self.__keyboard.release(Key.shift)
            elif key.isdigit():
                self.__keyboard.press(key)
                self.__keyboard.release(key)

    def write_line_lower(self, sentence):
        sentence = sentence.lower()
        self.__keyboard.type(sentence)

    def write_line(self, sentence):
       self.__keyboard.type(sentence)

    def enter(self):
        self.__keyboard.press(Key.enter)
        self.__keyboard.release(Key.enter)

    def down(self):
        self.__keyboard.press(Key.down)
        self.__keyboard.release(Key.down)

    def select_line(self):
        self.__keyboard.press(Key.shift)
        self.__keyboard.press(Key.ctrl)
        self.__keyboard.press(Key.right)
        self.__keyboard.release(Key.right)
        self.__keyboard.release(Key.ctrl)
        self.__keyboard.release(Key.shift)

    def delete(self):
        self.__keyboard.press(Key.delete)
        self.__keyboard.release(Key.delete)

    def save(self):
        with self.__keyboard.pressed(Key.ctrl):
            self.__keyboard.press('g')
            self.__keyboard.release('g')

    def select_all(self):
        with self.__keyboard.pressed(Key.ctrl):
            self.__keyboard.press('e')
            self.__keyboard.release('e')
