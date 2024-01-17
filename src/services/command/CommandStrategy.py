from abc import ABC, abstractmethod
from src.services.command.CommandExecutor import (WindowsVol2Executor,
                                                  WindowsVol3Executor,
                                                  LinuxVol2Executor,
                                                  LinuxVol3Executor)


class CommandStrategy(ABC):
    @abstractmethod
    def get_executor(self, os_type, forensic_tool):
        """
        Método abstracto para obtener un ejecutor de comando.
        Debe ser implementado por subclases específicas para cada sistema operativo.
        """
        pass


class WindowsFactory(CommandStrategy):
    def get_executor(self, os_type, forensic_tool):
        """
        Devuelve un ejecutor de comando apropiado para Windows según la herramienta forense especificada.

        Args:
            os_type (int): Tipo de sistema operativo (no utilizado en esta implementación).
            forensic_tool (int): Identificador de la herramienta forense (1 para Vol 2, 2 para Vol 3).

        Returns:
            CommandExecutor: Una instancia de WindowsVol2Executor o WindowsVol3Executor.

        Raises:
            ValueError: Si se proporciona una combinación no válida de sistema operativo y herramienta forense.
        """
        if forensic_tool == 1:  # Vol 2
            return WindowsVol2Executor()
        elif forensic_tool == 2:  # Vol 3
            return WindowsVol3Executor()
        else:
            raise ValueError("Combinación no válida de sistema operativo y forensic tool para Windows.")


class LinuxFactory(CommandStrategy):
    def get_executor(self, os_type, forensic_tool):
        """
        Devuelve un ejecutor de comando apropiado para Linux según la herramienta forense especificada.

        Args:
            os_type (int): Tipo de sistema operativo (no utilizado en esta implementación).
            forensic_tool (int): Identificador de la herramienta forense (1 para Vol 2, 2 para Vol 3).

        Returns:
            CommandExecutor: Una instancia de LinuxVol2Executor o LinuxVol3Executor.

        Raises:
            ValueError: Si se proporciona una combinación no válida de sistema operativo y herramienta forense.
        """
        if forensic_tool == 1:  # Vol 2
            return LinuxVol2Executor()
        elif forensic_tool == 2:  # Vol 3
            return LinuxVol3Executor()
        else:
            raise ValueError("Combinación no válida de sistema operativo y forensic tool para Linux.")


class CommandFactory(CommandStrategy):
    def get_executor(self, os_type, forensic_tool):
        """
        Devuelve un ejecutor de comando adecuado según el sistema operativo y la herramienta forense.

        Args:
            os_type (int): Tipo de sistema operativo (1 para Windows, 2 para Linux).
            forensic_tool (int): Identificador de la herramienta forense.

        Returns:
            CommandExecutor: Una instancia de un ejecutor de comando específico.

        Raises:
            ValueError: Si se proporciona una combinación no válida de sistema operativo y herramienta forense.
        """
        if os_type == 1:  # Windows
            return WindowsFactory.get_executor(self, os_type, forensic_tool)

        elif os_type == 2:  # LINUX
            return LinuxFactory.get_executor(self, os_type, forensic_tool)

        else:
            raise ValueError("Error al determinar el executor de comandos")
