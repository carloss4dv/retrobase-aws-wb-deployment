import multiprocessing
import subprocess
import signal
import time
import os
import sys
import pygetwindow as gw
from lib.window import Window
from lib.keyboard import Keyboard

delayScreen = 0.6
file = "./Database-MSDOS/Database/salida.txt"
name = "DOSBox 0.74, Cpu speed: max 100% cycles, Frameskip  0, Program:  GWBASIC"
confName = "dosbox-0.74.conf: Bloc de notas"
confNameEngw11 = "dosbox-0.74.conf - Notepad"
iReg = 13

class Singleton(type):
    __instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]

class Database(metaclass=Singleton):
    def __conf_emulator(self):
        options = subprocess.Popen(
            'cd .\\Database-MSDOS\\DOSBox-0.74 && ".\\DOSBox 0.74 Options.bat"',
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        tries = 0
        while not self.__check_window(confNameEngw11):
            if tries > 3:
                print("Not found...")
                sys.exit(0)
            print("Waiting for the DOSBox conf window to open please wait...")
            time.sleep(1)
            tries = tries + 1
        window = Window(confNameEngw11)
        self.__keyboard = Keyboard()
        #Delete previous conf
        self.__keyboard.select_all()
        self.__keyboard.delete()
        #Type new conf
        #[sdl]
        self.__keyboard.write_line("[sdl]\n\nfullscreen=false\nfulldouble=false\nfullresolution=original\nwindowresolution=original\noutput=surface\nautolock=true\nsensitivity=100\nwaitonerror=true\npriority=higher,normal\nmapperfile=mapper-0.74.map\nusescancodes=true\n\n")

        #[dosbox]
        self.__keyboard.write_line("[dosbox]\n\nlanguage=\nmachine=svga_s3\ncaptures=capture\nmemsize=16\n\n")

        #[render]
        self.__keyboard.write_line("[render]\n\nframeskip=0\naspect=false\nscaler=normal2x\n\n")

        #[cpu]
        self.__keyboard.write_line("[cpu]\n\ncore=auto\ncputype=auto\ncycles=max\ncycleup=10\ncycledown=20\n\n")

        #[mixer]
        self.__keyboard.write_line("[mixer]\n\nnosound=false\nrate=44100\nblocksize=1024\nprebuffer=20\n\n")

        self.__keyboard.save()

        time.sleep(3)
        options.terminate()
        window.close_window()
        del window
        
        
    # Private methods to handle the exit from the emulator
    def __close_windows(self) -> None:
        if self.__window != None:
            self.__window.close_window()
            self.__window = None
            self.__database.terminate()
            self.__database = None


    def __close_app(self) -> None:
        if self.__read:
            #We need to erase the temp file
            if os.path.exists(file):
                os.remove(file)
            if self.__check_window(name):
                self.__close_windows()

    def __check_window(self,check) -> bool:
        open_windows = gw.getWindowsWithTitle(check)
        return len(open_windows) > 0
    
    def __get_reg_by_name(self, name: str) -> int | None:
        print(f"Buscando el numero de registro del programa: {name}")
        result = None
        for entry in self.__regs["data"]:
            print(f"{entry['Name']}")
            if entry["Name"].lower() == name.lower():
                result = entry["Reg"]
            
        print(f"El numero de registro del programa {name} es {str(result)}")                 
        return result
    
    def __get_program_by_tape(self, tape: str):
        programs_in_tape = []
        for entry in self.__regs["data"]:
            tapes = entry["Tape"].split("-")
            if tape in tapes:
                programs_in_tape.append(entry)
        return programs_in_tape
        

    def __read_single_register(self, program_reg: int):
        print(f"Buscando el programa: ",program_reg)
        #Get single register
        self.__keyboard.press('7')  # Search option
        time.sleep(delayScreen)
        self.__keyboard.press('S')
        time.sleep(delayScreen)
        self.__keyboard.enter()
        time.sleep(delayScreen)
        self.__keyboard.write_line(str(program_reg))
        time.sleep(delayScreen)
        self.__keyboard.enter()
        time.sleep(delayScreen)
        self.__keyboard.press('S')
        time.sleep(delayScreen)
        self.__keyboard.enter()
        time.sleep(delayScreen)
        self.__keyboard.press('N')
        time.sleep(delayScreen)
        self.__keyboard.enter()
        time.sleep(delayScreen)
        self.__keyboard.press('N')
        time.sleep(delayScreen)
        self.__keyboard.enter()
        time.sleep(delayScreen)
        
        #Write the file thats used for redirection
        self.__keyboard.press('8')
        time.sleep(delayScreen)
        self.__keyboard.press('S')
        time.sleep(delayScreen)
        self.__keyboard.enter()
        time.sleep(delayScreen)
        self.__keyboard.write_line_lower('LIST')
        time.sleep(delayScreen)
        self.__keyboard.enter()
        time.sleep(delayScreen)
        self.__keyboard.write_line_lower('RUN')
        time.sleep(delayScreen)
        self.__keyboard.enter()
        time.sleep(delayScreen)
        self._read = True
        print(f"Proceso de búsqueda completado para:",program_reg)
        
    def __process_single_register(self):
        with open(file,"r") as fd:
            lines = fd.readlines()
            print(lines[iReg])
            line = lines[iReg].split()
            print(line)
            self.__single_reg = [{
                "Number": line[0],
                "Name": " ".join(line[2:-2]),
                "Type": line[-2],
                "Tape": line[-1].split(":")[1]
            }]

            print(line)
    

    def __read_file(self) -> None:
        self.__keyboard.press('6')
        time.sleep(delayScreen)
        self.__keyboard.enter()
        time.sleep(delayScreen)

        i = 1
        while i <= 43:
            self.__keyboard.press(' ')
            time.sleep(delayScreen)
            i = i + 1

        self.__keyboard.press('8')
        time.sleep(delayScreen)
        self.__keyboard.press('S')
        time.sleep(delayScreen)
        self.__keyboard.enter()
        time.sleep(delayScreen)
        self.__keyboard.write_line_lower('LIST')
        time.sleep(delayScreen)
        self.__keyboard.enter()
        time.sleep(delayScreen)
        self.__keyboard.write_line_lower('RUN')
        time.sleep(delayScreen)
        self.__keyboard.enter()
        time.sleep(delayScreen)
        self._read = True

    def __process_database(self) -> None:
        with open(file, "r") as fd:
            lines = fd.readlines()
            i = 15
            id = 1
            while (lines[i].strip() != "1 - INTRODUCIR DATOS"):
                self.__regs["data"].append({
                    "Number": id,
                    "Name": lines[i].strip(),
                    "Type": lines[i + 1],
                    "Tape": lines[i + 2].strip(),
                    "Reg": lines[i + 3].strip()})
                i = i + 5
                id = id + 1
            
            self.__regs["total_reg"] = id
        

    def __get_only_program_names(self) -> list:
        return [entry["Name"] for entry in self.__regs["data"]]

    def __init_emulator(self) -> None:
        print("Configuring emulator...")
        # self.__conf_emulator()
        self.__keyboard = Keyboard()
        print("Success")
        #Check if process is open 
        if self.__check_window(name):
            self.__close_windows()
        
        self.__database = subprocess.Popen(
            "cd .\\Database-MSDOS && .\\database.bat > salida.txt",
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)
        tries = 0
        while not self.__check_window(name):
            if tries > 5:
                self.__close_app()
                sys.exit(0)
            print("Waiting for the DOSBox window to open please wait...")
            time.sleep(1)
            tries = tries + 1
        self.__window = Window(name)
        self.__read = False

    def __get_all_registers(self) -> None:
        self.__regs = {
            "total_reg": 0,
            "data": []
        }
        self.__read_file()
        self.__process_database()
        self.__close_windows()
        self.__close_app()

    def __init__(self):
        self.__single_reg = []
        self.__regs = {
            "total_reg": 0,
            "data": []
        }
        self.__read = False
        self.__window = None
        self.__database = None
        self._keyboard = None
        


    # Public methods
    def get_programs(self) -> list:
        # return self.__get_only_program_names()
        self.__init_emulator()
        print("Emulator initiated with no errors")
        self.__get_all_registers()
        print("Database stored with 0 errors")
        return self.__regs["data"]
    
    def get_programs_by_tape(self, tape: str) -> list:
        return self.__get_program_by_tape(tape)

    def get_specific_program_data(self, program_name: str):
        self.__init_emulator()
        self.__read_single_register(self.__get_reg_by_name(program_name))
        self.__process_single_register()
        self.__close_windows()
        self.__close_app()  
        
        return self.__single_reg

    def get_total_reg_count(self) -> int:
        return self.__regs["total_reg"]
    
    def see_raw_data(self):
        return self.__regs["data"]
    
    
