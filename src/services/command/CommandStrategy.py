from abc import ABC, abstractmethod
from src.services.command.CommandExecutor import (WindowsVol2Executor,
                                                  WindowsVol3Executor,
                                                  LinuxVol2Executor,
                                                  LinuxVol3Executor)


class CommandStrategy(ABC):
    @abstractmethod
    def get_executor(self, os_type, forensic_tool):
        pass


class WindowsFactory(CommandStrategy):
    def get_executor(self, os_type, forensic_tool):
        if forensic_tool == 1:  # Vol 2
            return WindowsVol2Executor()
        elif forensic_tool == 2:  # Vol 3
            return WindowsVol3Executor()
        else:
            raise ValueError("Combinación no válida de sistema operativo y forensic tool para Windows.")


class LinuxFactory(CommandStrategy):
    def get_executor(self, os_type, forensic_tool):
        if forensic_tool == 1:  # Vol 2
            return LinuxVol2Executor()
        elif forensic_tool == 2:  # Vol 3
            return LinuxVol3Executor()
        else:
            raise ValueError("Combinación no válida de sistema operativo y forensic tool para Linux.")


class CommandFactory(CommandStrategy):
    def get_executor(self, os_type, forensic_tool):
        if os_type == 1:  # Windows
            return WindowsFactory.get_executor(self, os_type, forensic_tool)

        elif os_type == 2:  # LINUX
            return LinuxFactory.get_executor(self, os_type, forensic_tool)

        else:
            raise ValueError("Error al determinar el executor de comandos")

"""
    if forensic_tool == 1 or forensic_tool == 2: # Vol2 y Vol3 respectivamente
        if forensic_tool == 1:  # Vol2
            if os_type == 1:  # Windows
                return LinuxVolatility2Executor()
            elif os_type == 2:  # Linux
                return LinuxVolatility3Executor()
        elif forensic_tool == 2:  # Vol3
            if os_type == 1:  # Windows
                return LinuxVolatility2Executor()
            elif os_type == 2:  # Linux
                return LinuxVolatility3Executor()
    else:
        raise ValueError("Error al determinar el executor de comandos")
"""